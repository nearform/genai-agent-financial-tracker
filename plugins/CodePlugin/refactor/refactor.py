import json
from io import StringIO
import yfinance as yf
import pandas as pd
from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.functions.function_result import FunctionResult


class CodeRefactor:




    @kernel_function(name="refactor", description="refactors a piece of code to include the provided dataFrame")
    def refactor(
        self,
        code:Annotated[str, "The code to be refactored"],
        data:Annotated[str, "The pandas dataFrame to be included in the code"],
        TICKER_AND_PERIOD: Annotated[str, "The ticker name and period provided on the initial input"]):
        args = json.loads(TICKER_AND_PERIOD)
        ticker_name =  args["ticker_name"]
        period =  args["period"] if args["period"] is not None else "1y"
        
        code = code.strip('```python')
        code = code.strip('```')
        code = code.replace('# df=TEMP_DATA', f'df = pd.read_json(StringIO(\'{data}\'), orient="split")')
        code = code.replace('TITLE',f'{ticker_name} stock over the period of {period}')
        return code

