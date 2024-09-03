# Assuming parse_tool_response is defined as given in the question
from parsing import parse_tool_response


def test_parse_tool_response():
    # Given response string from LLM
    response = (
        '<function=generate_character>{"name": "John Doe", '
        '"description": "A 35-year-old software engineer from Seattle.", '
        '"personality": "Introverted, analytical, and detail-oriented.", '
        '"profile": "John is a skilled programmer who enjoys solving complex problems. '
        'He has a passion for technology and is always looking to learn new skills.", '
        '"likes": "Coding, video games, reading science fiction novels.", '
        '"dislikes": "Small talk, crowded places, public speaking.", '
        '"first message": "Hey there! I\'m John, a software engineer who loves all things tech.", '
        '"speech patterns": "John speaks in a calm and measured tone. '
        'He often uses technical jargon and strives to be precise in his language."}'
        '</function>'
    )

    # Expected output
    expected_output = {
        "function": "generate_character",
        "arguments": {
            "name": "John Doe",
            "description": "A 35-year-old software engineer from Seattle.",
            "personality": "Introverted, analytical, and detail-oriented.",
            "profile": "John is a skilled programmer who enjoys solving complex problems. He has a passion for technology and is always looking to learn new skills.",
            "likes": "Coding, video games, reading science fiction novels.",
            "dislikes": "Small talk, crowded places, public speaking.",
            "first message": "Hey there! I'm John, a software engineer who loves all things tech.",
            "speech patterns": "John speaks in a calm and measured tone. He often uses technical jargon and strives to be precise in his language."
        }
    }

    # Actual result from parse_tool_response
    actual_result = parse_tool_response(response)

    # Assert that the actual result matches the expected output
    assert actual_result == expected_output
