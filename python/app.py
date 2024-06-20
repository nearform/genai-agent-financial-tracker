# Copyright (c) Microsoft. All rights reserved.

import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.functions import KernelArguments
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior

from plugins.CodePlugin.refactor.refactor import CodeRefactor
from plugins.FinancePlugin.finance import FinancePlugin
from semantic_kernel.planners import SequentialPlanner


#Boilerplate
kernel = Kernel()

useAzureOpenAI = False
ai_model_id="gpt-3.5-turbo"
service_id = "chat"
execution_settings = OpenAIChatPromptExecutionSettings(
    service_id="chat"
)

# Configure AI service used by the kernel
kernel.add_service(
    OpenAIChatCompletion(service_id=service_id,ai_model_id=ai_model_id),
)

#Adding our defined plugins
kernel.add_plugin(parent_directory="./plugins", plugin_name="ChatPlugin")
kernel.add_plugin(plugin=FinancePlugin(), plugin_name="FinancePlugin")
kernel.add_plugin(parent_directory="./plugins", plugin_name="ChartPlugin")
kernel.add_plugin(plugin=CodeRefactor(), plugin_name="CodePlugin")

async def chat(planner):
    try:
        user_input = input("User: ")
        if user_input == "exit":
            print("\n\nExiting chat...")
            return False
        return await get_planner(planner, user_input)
    except KeyboardInterrupt:
        print("\n\nExiting chat...")
        return False
    except EOFError:
        print("\n\nExiting chat...")
        return False
   
    
async  def get_planner(planner,user_input:str):
    try:
        arguments = KernelArguments(settings=execution_settings)
        arguments["user_input"]= user_input
        goal = f'Based on the user_input argument,chat with the AI to get the ticker_name and period if available, extract the data for a ticker over time, create a drawdown, plot the chart, refactor the code to include the drawdow data.'
        plan = await planner.create_plan(goal = goal)
        result = await plan.invoke(kernel=kernel, arguments=arguments)

        exec(str(result))
        return True
    except Exception as e:
        print('There has been a problem running the code')
        return True



async def main() -> None:
    chatting = True
   
    planner = SequentialPlanner(service_id=service_id, kernel=kernel)
   
    print(
        "Welcome to the financial chat bot!\
        Ask to get details on the stock of a company \
        \n  Type 'exit' to exit."
    )
    while chatting:
        chatting = await chat(planner)




if __name__ == "__main__":
    asyncio.run(main())
