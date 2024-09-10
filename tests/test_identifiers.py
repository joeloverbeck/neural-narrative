import json
from unittest.mock import mock_open, patch

from src.enums import IdentifierType
from src.identifiers import determine_next_identifier


def test_determine_next_identifier_characters():
    # Mock content of last_identifiers.json
    mock_json_data = json.dumps({"last_identifiers": {
        "characters": "0",
        "places": "5"
    }})

    # Use unittest.mock to mock open() and simulate reading the JSON file
    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        # Call the function with the enum for CHARACTERS
        next_identifier = determine_next_identifier("some_playthrough", IdentifierType.CHARACTERS)

        # Assert that the returned value is 1 (0 + 1)
        assert next_identifier == 1
