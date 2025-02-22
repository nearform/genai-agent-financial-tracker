import json
from io import StringIO
import numpy as np
import yfinance as yf
import pandas as pd
from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.functions.function_result import FunctionResult

class FinancePlugin:

    @kernel_function(name="financial_info", description="gets the details for a stock")
    def financial_info(
        self,
        TICKER_AND_PERIOD):
        if not TICKER_AND_PERIOD:
            raise Exception("No ticker value provided")
        args = json.loads(TICKER_AND_PERIOD)
        ticker_name =  args["ticker_name"]
        period =  args["period"]
        if ticker_name is not None:    
            ticker = yf.Ticker(ticker_name)
            time = period if period is not None else '1y'
            data = ticker.history(period = time)
            data = data.drop(columns=["Open","High","Low","Volume", "Dividends", "Stock Splits"])
            data.index = data.index.strftime('%Y-%m-%d')
            data["Close"] = data["Close"].round(4)
            print('data retrieval complete')
            return data.to_json()

    @kernel_function(name="drawdown", description="Calculate the drawdown values for the stock")
    def drawdown(self, data_json: Annotated[str, "the data from the stock"]):

        data =  pd.read_json(StringIO(data_json))
        data['Peak'] = data['Close'].cummax()
        data['Drawdown'] = data['Close'] - data['Peak']
        data["Drawdown"] = data["Drawdown"].round(4)
        data = data.drop(columns=["Peak"])
        print('drawdown calculated')
        return str(data.to_json(orient='split'))