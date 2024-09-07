from typing import List, Optional

from src.constants import TOOL_INSTRUCTIONS_FILE
from src.files import read_file, read_json_file
from src.tools import generate_tool_prompt


def does_response_contain_message(completion):
    return completion.choices and completion.choices[0] and completion.choices[0].message


def is_valid_response(completion):
    return does_response_contain_message(completion) and completion.choices[0].message.content


def prompt_for_character_identifier(prompt_text: str) -> Optional[int]:
    """Prompt user for a character identifier, allow empty input."""
    user_input = input(prompt_text)
    if user_input.strip() == "":
        return None  # If input is empty, return None
    try:
        return int(user_input)  # Convert input to integer
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return prompt_for_character_identifier(prompt_text)  # Retry


def prompt_for_multiple_identifiers(prompt_text: str) -> List[int]:
    """Prompt for multiple character identifiers."""
    while True:
        user_input = input(prompt_text)
        if user_input.strip() == "":
            return []  # If no input, return an empty list

        # Try to convert input to a list of integers
        try:
            # Split the input by space or comma and strip spaces
            identifiers = [int(x.strip()) for x in user_input.replace(",", " ").split() if x.strip()]
            return identifiers
        except ValueError:
            print("Invalid input. Please enter valid integers separated by spaces or commas.")


def prompt_for_input(prompt_text: str) -> str:
    """Prompt user for input until valid data is provided."""
    while True:
        user_input = input(prompt_text)
        if user_input:
            return user_input
        else:
            print(f"{prompt_text} cannot be empty. Please try again.")


def create_system_content_for_dialogue_prompt(participants: List[dict], character_data: dict, memories: str,
                                              prompt_file: str,
                                              tool_file: str) -> str:
    """Format system content using character data and memories."""
    prompt_template = read_file(prompt_file)
    tool_data = read_json_file(tool_file)

    # It's necessary to format some of the values in tool_data with actual values.
    replacements = {
        "name": character_data["name"]
    }

    tool_data['function']['description'] = tool_data['function']['description'].format(**replacements)
    tool_data['function']['parameters']['properties']['narration_text']['description'] = \
        tool_data['function']['parameters']['properties']['narration_text']['description'].format(**replacements)
    tool_data['function']['parameters']['properties']['name']['description'] = \
        tool_data['function']['parameters']['properties']['name']['description'].format(**replacements)
    tool_data['function']['parameters']['properties']['speech']['description'] = \
        tool_data['function']['parameters']['properties']['speech']['description'].format(**replacements)

    participant_details = "\n".join(
        [f'{participant["name"]}: {participant["description"]}' for participant in participants if
         participant["name"] != character_data["name"]])

    return prompt_template.format(
        name=character_data["name"],
        participant_details=participant_details,
        description=character_data["description"],
        personality=character_data["personality"],
        profile=character_data["profile"],
        likes=character_data["likes"],
        dislikes=character_data["dislikes"],
        first_message=character_data["first message"],
        speech_patterns=character_data["speech patterns"],
        memories=memories
    ) + "\n\n" + generate_tool_prompt(tool_data, read_file(TOOL_INSTRUCTIONS_FILE))
