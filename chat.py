import colorama
from openai import OpenAI

# Import from local modules
from src.constants import OPENROUTER_API_URL
from src.dialogues.commands.store_dialogues_command import StoreDialoguesCommand
from src.dialogues.dialogues import summarize_dialogue
from src.dialogues.factories.concrete_dialogue_factory import ConcreteDialogueFactory
from src.dialogues.observers.console_dialogue_observer import ConsoleDialogueObserver
from src.files import load_secret_key
from src.prompting.prompting import prompt_for_input, prompt_for_character_identifier, prompt_for_multiple_identifiers


def main():
    colorama.init()

    playthrough_name = prompt_for_input("Enter your playthrough name: ")

    # Prompt for user's own character identifier (optional)
    player_identifier = prompt_for_character_identifier("Enter your character identifier (can be empty): ")

    # Prompt for character(s) the user wishes to speak to
    participants = prompt_for_multiple_identifiers(
        "Enter the identifiers of the characters you wish to speak to (separated by spaces or commas): ")

    if player_identifier:
        participants.insert(0, player_identifier)

    # gets API Key from environment variable OPENAI_API_KEY
    client = OpenAI(
        base_url=OPENROUTER_API_URL,
        api_key=load_secret_key(),
    )

    concrete_dialogue_factory = ConcreteDialogueFactory(client, playthrough_name, participants, player_identifier)

    concrete_dialogue_factory.attach(ConsoleDialogueObserver())

    dialogue_product = concrete_dialogue_factory.create_dialogue()

    summarize_dialogue(playthrough_name, client, participants, dialogue_product.get())

    StoreDialoguesCommand(playthrough_name, participants, dialogue_product.get()).execute()


if __name__ == "__main__":
    main()
