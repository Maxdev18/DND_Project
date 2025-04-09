from util.llm_utils import tool_tracker

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