import pytest

from src.prompting.function_call_sanitizer import FunctionCallSanitizer


@pytest.mark.parametrize(
    "response, expected_response",
    [
        (
            '    <function=test> {"arg": 1}  </function>  ',
            '<function=test>{"arg": 1}</function>',
        ),
        (
            '\n<function=test> {"arg": 1}\n</function>\n',
            '<function=test>{"arg": 1}</function>',
        ),
        (
            '<function=test> {"arg": 1}}</function>',
            '<function=test>{"arg": 1}</function>',
        ),
    ],
)
def test_fix_tool_call(response, expected_response):
    provider = FunctionCallSanitizer(response)

    assert provider.sanitize() == expected_response


def test_sanitize_response():
    response = (
        '<function=generate_region>{"name": "Nexoria", "description": '
        '"Nexoria is a region defined by its sprawling savannas and vast grasslands, '
        "interrupted by towering mountain ranges and deep, winding canyons. The climate "
        "is mostly warm and temperate, with mild winters and hot summers. The region is "
        "home to a diverse array of sentient species, including lion folk, elephant men, "
        "and giraffe people, among others. The cultural norms of Nexoria revolve around "
        "community and cooperation, with a strong emphasis on hospitality and mutual aid. "
        "Music and dance are integral to their way of life, with vibrant festivals held "
        "throughout the year to celebrate the changing seasons and the bounty of the land."
        "The architecture of Nexoria is characterized by its use of natural materials, "
        "such as wood, stone, and thatch, with buildings designed to blend seamlessly into "
        "the surrounding landscape. Iconic structures include the Great Boma, a massive "
        "circular meeting hall where the region's leaders gather to discuss matters of "
        "importance, and the Tower of Winds, a soaring spire adorned with intricate carvings "
        "that whistles hauntingly in the breeze.Nexoria is governed by a council of elders, "
        "with representatives from each of the region's major clans.\"}</function>"
    )

    expected_output = (
        '<function=generate_region>{"name": "Nexoria", "description": '
        '"Nexoria is a region defined by its sprawling savannas and vast grasslands, '
        "interrupted by towering mountain ranges and deep, winding canyons. The climate "
        "is mostly warm and temperate, with mild winters and hot summers. The region is "
        "home to a diverse array of sentient species, including lion folk, elephant men, "
        "and giraffe people, among others. The cultural norms of Nexoria revolve around "
        "community and cooperation, with a strong emphasis on hospitality and mutual aid. "
        "Music and dance are integral to their way of life, with vibrant festivals held "
        "throughout the year to celebrate the changing seasons and the bounty of the land.\\n"
        "The architecture of Nexoria is characterized by its use of natural materials, "
        "such as wood, stone, and thatch, with buildings designed to blend seamlessly into "
        "the surrounding landscape. Iconic structures include the Great Boma, a massive "
        "circular meeting hall where the region's leaders gather to discuss matters of "
        "importance, and the Tower of Winds, a soaring spire adorned with intricate carvings "
        "that whistles hauntingly in the breeze.\\nNexoria is governed by a council of elders, "
        "with representatives from each of the region's major clans.\"}</function>"
    )

    parser = FunctionCallSanitizer(response)

    assert parser.sanitize() == expected_output


def test_no_fix_needed():
    response = '<function=generate_region>{"name": "Nexoria", "description": "This is correct."}</function>'
    expected_output = response

    parser = parser = FunctionCallSanitizer(response)

    assert parser.sanitize() == expected_output


import pytest
import re
import json


def test_function_call_sanitizer_handles_incorrect_closing_tag():
    function_call_input = """<function=generate_interesting_situations>{"interesting_situations": ["Audrey discovers that Alain's family emergency was a ruse and he is actually on a secret mission, putting her in a position to help him despite their complicated past.", "Alain returns home early and overhears the conversation between Audrey and Luc, leading to an emotional confrontation and difficult choices for all three characters.", "Luc, feeling threatened by Audrey's presence and her history with Alain, starts scheming to drive a wedge between them permanently.", "Audrey uncovers a hidden secret about Luc that could change everything, forcing her to decide whether to use this information to win back Alain or to do the right thing.", "An unexpected event forces Audrey, Alain, and Luc to work together, testing their loyalty and feelings for each other in a high-stakes situation."]}[/function]"""

    # Create an instance of FunctionCallSanitizer
    sanitizer = FunctionCallSanitizer(function_call_input)

    # Sanitize the function call
    sanitized_output = sanitizer.sanitize()

    # Regex to extract function name and JSON data
    function_call_pattern = re.compile(r"<function=(\w+)>(\{.*})</function>")

    match = function_call_pattern.match(sanitized_output)
    assert match is not None, "Sanitized output did not match expected pattern"

    function_name = match.group(1)
    json_data_str = match.group(2)

    # Check that function name is correct
    assert function_name == "generate_interesting_situations"

    # Try to parse JSON data
    try:
        json_data = json.loads(json_data_str)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON data: {e}")

    # Check that 'interesting_situations' is in the JSON data
    assert "interesting_situations" in json_data

    # Additional checks can be added to verify the content of 'interesting_situations'
    assert isinstance(json_data["interesting_situations"], list)
    assert len(json_data["interesting_situations"]) > 0
