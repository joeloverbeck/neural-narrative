import pytest

from src.prompting.function_call_sanitizer import FunctionCallSanitizer


@pytest.mark.parametrize("response, expected_response", [
    ("    <function=test> {\"arg\": 1}  </function>  ", "<function=test>{\"arg\": 1}</function>"),
    ("\n<function=test> {\"arg\": 1}\n</function>\n", "<function=test>{\"arg\": 1}</function>"),
    ("<function=test> {\"arg\": 1}}</function>", "<function=test>{\"arg\": 1}</function>"),
])
def test_fix_tool_call(response, expected_response):
    provider = FunctionCallSanitizer(response)

    assert provider.sanitize() == expected_response


def test_sanitize_response():
    response = (
        "<function=generate_region>{\"name\": \"Nexoria\", \"description\": "
        "\"Nexoria is a region defined by its sprawling savannas and vast grasslands, "
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
        "<function=generate_region>{\"name\": \"Nexoria\", \"description\": "
        "\"Nexoria is a region defined by its sprawling savannas and vast grasslands, "
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
    response = "<function=generate_region>{\"name\": \"Nexoria\", \"description\": \"This is correct.\"}</function>"
    expected_output = response

    parser = parser = FunctionCallSanitizer(response)

    assert parser.sanitize() == expected_output
