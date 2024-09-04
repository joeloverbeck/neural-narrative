import json
import os

from openai import OpenAI

from src.constants import CHARACTERS_FOLDER_NAME, PLAYTHROUGHS_FOLDER, CHARACTERS_FILE, OPENROUTER_API_URL, HERMES_405B, \
    CHARACTER_GENERATION_INSTRUCTIONS_FILE, CHARACTER_GENERATOR_TOOL_FILE
from src.enums import IdentifierType
from src.files import load_existing_or_new_json_file, save_json_file, read_file, load_secret_key
from src.identifiers import determine_next_identifier, store_last_identifier
from src.parsing import parse_tool_response
from src.tools import generate_tool_prompt


def generate_character(user_input_on_character: str):
    # Load the JSON file
    with open(CHARACTER_GENERATOR_TOOL_FILE, 'r') as file:
        character_generator_tool = json.load(file)

    # gets API Key from environment variable OPENAI_API_KEY
    client = OpenAI(
        base_url=OPENROUTER_API_URL,
        api_key=load_secret_key(),
    )

    completion = client.chat.completions.create(
        model=HERMES_405B,
        messages=[
            {
                "role": "system",
                "content": read_file(CHARACTER_GENERATION_INSTRUCTIONS_FILE) + "\n\n" + generate_tool_prompt(
                    character_generator_tool),
            },
            {
                "role": "user",
                "content": f"Create the bio for a character based in the post-apocalypse. {user_input_on_character}",
            },
        ],
        temperature=1.0,
        top_p=1.0,
    )

    if completion.choices and completion.choices[0] and completion.choices[0].message:
        return parse_tool_response(completion.choices[0].message.content)
    else:
        print("The LLM didn't return a valid message.")
        print(completion)


def store_generated_character(playthrough_name, character_data):
    # Build the path to the characters folder
    characters_folder = os.path.join(PLAYTHROUGHS_FOLDER, playthrough_name, CHARACTERS_FOLDER_NAME)
    os.makedirs(characters_folder, exist_ok=True)

    # Build the path to the characters.json file
    characters_file = os.path.join(characters_folder, CHARACTERS_FILE)

    characters = load_existing_or_new_json_file(characters_file)

    new_id = determine_next_identifier(playthrough_name, IdentifierType.CHARACTERS)

    # Given that a character is going to be added to file, the identifier on file for characters
    # should be changed.
    store_last_identifier(playthrough_name, IdentifierType.CHARACTERS, new_id)

    # Add the new character entry
    characters[new_id] = character_data

    save_json_file(characters, characters_file)
