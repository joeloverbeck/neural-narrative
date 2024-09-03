import json


def generate_tool_prompt(tool):
    return f"""
    You have access to the following functions:

    Use the function '{tool["name"]}' to '{tool["description"]}':
    {json.dumps(tool)}

    If you choose to call a function ONLY reply in the following format with no prefix or suffix:

    <function=example_function_name>{{\"example_name\": \"example_value\"}}</function>

    Reminder:
    - Function calls MUST follow the specified format, start with <function= and end with </function>
    - Required parameters MUST be specified
    - Only call one function at a time
    - Put the entire function call reply on one line
    - If there is no function call available, answer the question like normal with your current knowledge and do not tell the user about function calls
    """
