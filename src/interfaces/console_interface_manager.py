from typing import Optional


class ConsoleInterfaceManager:

    def prompt_for_character_identifier(self, prompt_text: str) -> Optional[str]:
        """Prompt user for a character identifier, allow empty input."""
        user_input = input(prompt_text)
        if user_input.strip() == "":
            return None
        try:
            character_identifier = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            return self.prompt_for_character_identifier(prompt_text)
        return str(character_identifier)

    @staticmethod
    def prompt_for_input(prompt_text: str) -> str:
        """Prompt user for input until valid data is provided."""
        while True:
            user_input = input(prompt_text)
            if user_input:
                return user_input
            else:
                print(f"{prompt_text} cannot be empty. Please try again.")
