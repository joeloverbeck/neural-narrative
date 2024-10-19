import json


def generate_tool_prompt(tool: dict, tool_instructions_template: str):
    assert tool

    return tool_instructions_template.format(tool_name=tool["function"]["name"],
                                             tool_description=tool["function"]["description"],
                                             tool=json.dumps(tool["function"]))
