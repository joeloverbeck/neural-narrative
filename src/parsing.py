import json
import re


def parse_tool_response(response: str):
    function_regex = r"<function=(\w+)>(.*?)</function>"
    match = re.search(function_regex, response)

    if match:
        function_name, args_string = match.groups()
        try:
            args = json.loads(args_string)
            return {
                "function": function_name,
                "arguments": args,
            }
        except json.JSONDecodeError as error:
            print(f"Error parsing function arguments: {error}")
            return None
    return None


def extract_character_from_tool_response(parsed_tool_response):
    # Extract the "arguments" dictionary from the tool response
    arguments = parsed_tool_response.get("arguments", {})

    # Build the result JSON from the extracted fields
    parsed_json = {
        "name": arguments.get("name"),
        "description": arguments.get("description"),
        "personality": arguments.get("personality"),
        "profile": arguments.get("profile"),
        "likes": arguments.get("likes"),
        "dislikes": arguments.get("dislikes"),
        "first message": arguments.get("first message"),
        "speech patterns": arguments.get("speech patterns")
    }

    return parsed_json
