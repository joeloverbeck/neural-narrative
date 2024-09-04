import json
import os

from src.constants import PLAYTHROUGHS_FOLDER, LAST_IDENTIFIERS_FILE
from src.enums import IdentifierType
from src.files import load_existing_or_new_json_file, save_json_file


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


def store_last_identifier(playthrough_name: str, identifier_type: IdentifierType, new_identifier: int):
    """
    Store the last identifier for the given identifier type in the JSON file.

    Args:
        playthrough_name (str): The name of the playthrough to which this identifier corresponds.
        identifier_type (IdentifierType): The type of identifier to update (e.g., places or characters).
        new_identifier (int): The new identifier to store.

    """
    # Define the file path
    file_path = os.path.join(PLAYTHROUGHS_FOLDER, playthrough_name, LAST_IDENTIFIERS_FILE)

    # Load the existing JSON data
    json_data = load_existing_or_new_json_file(file_path)

    # Update the identifier based on the identifier type
    if identifier_type == IdentifierType.CHARACTERS:
        json_data["characters"] = str(new_identifier)
    elif identifier_type == IdentifierType.PLACES:
        json_data["places"] = str(new_identifier)

    # Save the updated JSON data back to the file
    save_json_file(json_data, file_path)
