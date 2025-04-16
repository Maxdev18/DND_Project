from util.llm_utils import run_console_chat, tool_tracker
from tools import *

@tool_tracker
def process_function_call(function_call):
    name = function_call.name
    args = function_call.arguments

    return globals()[name](**args)

def process_response(self, response):
    if response.message.tool_calls:
        result = process_function_call(response.message.tool_calls[0].function)
        self.messages.append({
            'role': 'tool',
            'name': response.message.tool_calls[0].function.name, 
            'arguments': response.message.tool_calls[0].function.arguments,
            'content': result
        })
        response = self.completion()

    return response

def main():
    run_console_chat(template_file='util/templates/dm_chat.json',
                 process_response=process_response)
  
if __name__ == "__main__":
  main()