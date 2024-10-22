from src.prompting.providers.concrete_tool_response_parsing_provider import ConcreteToolResponseParsingProvider


def test_parse_tool_response():
    response = (
        '<function=generate_character>{"name": "John Doe", "description": "A 35-year-old software engineer from Seattle.", "personality": "Introverted, analytical, and detail-oriented.", "profile": "John is a skilled programmer who enjoys solving complex problems. He has a passion for technology and is always looking to learn new skills.", "likes": "Coding, video games, reading science fiction novels.", "dislikes": "Small talk, crowded places, public speaking.", "first message": "Hey there! I\'m John, a software engineer who loves all things tech.", "speech patterns": "John speaks in a calm and measured tone. He often uses technical jargon and strives to be precise in his language."}</function>'
    )
    expected_output = {'function': 'generate_character', 'arguments': {
        'name': 'John Doe', 'description':
            'A 35-year-old software engineer from Seattle.', 'personality':
            'Introverted, analytical, and detail-oriented.', 'profile':
            'John is a skilled programmer who enjoys solving complex problems. He has a passion for technology and is always looking to learn new skills.'
        , 'likes': 'Coding, video games, reading science fiction novels.',
        'dislikes': 'Small talk, crowded places, public speaking.',
        'first message':
            "Hey there! I'm John, a software engineer who loves all things tech.",
        'speech patterns':
            'John speaks in a calm and measured tone. He often uses technical jargon and strives to be precise in his language.'
    }}
    actual_result = ConcreteToolResponseParsingProvider(response
                                                        ).parse_tool_response()
    assert actual_result.is_valid()
    assert actual_result.get() == expected_output
