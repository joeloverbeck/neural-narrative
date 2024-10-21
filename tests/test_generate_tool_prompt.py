from src.base.required_string import RequiredString
from src.base.tools import generate_tool_prompt


def test_generate_tool_prompt_function():
    tool_data = {
        "function": {
            "name": "test_tool",
            "description": "A test tool",
        }
    }
    tool_instructions_template = RequiredString("Use {tool_name}: {tool_description}")
    expected_result = RequiredString("Use test_tool: A test tool")

    result = generate_tool_prompt(tool_data, tool_instructions_template)

    assert result == expected_result
