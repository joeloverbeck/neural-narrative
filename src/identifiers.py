import json
import os

from src.constants import PLAYTHROUGHS_FOLDER, LAST_IDENTIFIERS_FILE


def determine_next_identifier(playthrough_name: str, identifier_type):
    # Join the folder and file to get the full path
    file_path = os.path.join(PLAYTHROUGHS_FOLDER, playthrough_name, LAST_IDENTIFIERS_FILE)

    # Load the JSON file
    with open(file_path, "r") as f:
        last_identifiers = json.load(f)

    # Get the value based on the identifier type
    current_value = int(last_identifiers[identifier_type.value])

    # Increment the value by 1
    return current_value + 1
