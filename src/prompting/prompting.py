from typing import List, Optional


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
