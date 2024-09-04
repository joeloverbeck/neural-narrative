import sys

from src.constants import SECRET_KEY_FILE


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()


import json
import os


def load_existing_or_new_json_file(file_path):
    """
    Load existing data from a JSON file or create a new file if it doesn't exist.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file, either loaded or initialized as an empty dictionary.
    """
    # If the file doesn't exist, create it and write an empty dictionary to it
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump({}, f)

    # Load the existing data from the file
    with open(file_path, "r") as f:
        return json.load(f)


def save_json_file(json_data, file_path):
    # Write the updated data back to the file
    with open(file_path, "w") as f:
        json.dump(json_data, f, indent=4)


def load_secret_key():
    try:
        # Attempt to load the secret key
        return read_file(SECRET_KEY_FILE)
    except FileNotFoundError:
        sys.exit(f"Error: File '{SECRET_KEY_FILE}'not found. Please check the file path.")
    except Exception as e:
        sys.exit(f"An unexpected error occurred: {str(e)}")
