# Assuming parse_tool_response is defined as given in the question
from src.parsing import parse_tool_response, extract_character_from_tool_response


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


def test_extract_character_from_tool_response():
    parsed_tool_response = {
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

    # The expected JSON structure after the parsing function
    expected_json = {
        "name": "John Doe",
        "description": "A 35-year-old software engineer from Seattle.",
        "personality": "Introverted, analytical, and detail-oriented.",
        "profile": "John is a skilled programmer who enjoys solving complex problems. He has a passion for technology and is always looking to learn new skills.",
        "likes": "Coding, video games, reading science fiction novels.",
        "dislikes": "Small talk, crowded places, public speaking.",
        "first message": "Hey there! I'm John, a software engineer who loves all things tech.",
        "speech patterns": "John speaks in a calm and measured tone. He often uses technical jargon and strives to be precise in his language."
    }

    # Call the function to parse the character data from the tool's response
    parsed_json = extract_character_from_tool_response(parsed_tool_response)

    # Compare the parsed JSON with the expected JSON
    assert parsed_json == expected_json, f"Parsed JSON does not match expected output. Got: {parsed_json}"
