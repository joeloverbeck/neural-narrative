import json
import os


def create_playthrough(playthrough_name):
    # Path to the playthroughs folder
    playthroughs_folder = 'playthroughs'

    # Ensure the playthroughs folder exists
    if not os.path.exists(playthroughs_folder):
        os.makedirs(playthroughs_folder)

    # Path to the new playthrough folder
    playthrough_path = os.path.join(playthroughs_folder, playthrough_name)

    # Check if the folder already exists
    if os.path.exists(playthrough_path):
        raise Exception(f"A playthrough with the name '{playthrough_name}' already exists.")

    # Create the new playthrough folder
    os.makedirs(playthrough_path)

    # Create the 'last_identifiers' JSON file inside the playthrough folder
    last_identifiers = {
        "places": "0",
        "characters": "0"
    }

    # Path to the 'last_identifiers.json' file
    json_path = os.path.join(playthrough_path, 'last_identifiers.json')

    # Write the initial values to the JSON file
    with open(json_path, 'w') as f:
        json.dump(last_identifiers, f)

    return playthrough_path
