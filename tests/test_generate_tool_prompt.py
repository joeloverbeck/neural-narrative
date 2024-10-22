from src.base.tools import generate_tool_prompt


def test_generate_tool_prompt_function():
    tool_data = {'function': {'name': 'test_tool', 'description':
        'A test tool'}}
    tool_instructions_template = 'Use {tool_name}: {tool_description}'
    expected_result = 'Use test_tool: A test tool'
    result = generate_tool_prompt(tool_data, tool_instructions_template)
    assert result == expected_result
