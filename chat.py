import colorama
from openai import OpenAI

from src.characters.commands.summarize_dialogue_command import SummarizeDialogueCommand
# Import from local modules
from src.constants import OPENROUTER_API_URL, HERMES_405B
from src.dialogues.commands.store_dialogues_command import StoreDialoguesCommand
from src.dialogues.factories.concrete_dialogue_factory import ConcreteDialogueFactory
from src.dialogues.observers.console_dialogue_observer import ConsoleDialogueObserver
from src.dialogues.strategies.concrete_involve_player_in_dialogue_strategy import \
    ConcreteInvolvePlayerInDialogueStrategy
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.prompting import prompt_for_input, prompt_for_character_identifier, prompt_for_multiple_identifiers


def main():
    colorama.init()

    playthrough_name = prompt_for_input("Enter your playthrough name: ")

    filesystem_manager = FilesystemManager()

    location_file = filesystem_manager.load_existing_or_new_json_file(
        filesystem_manager.get_file_path_to_locations_template_file())

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
        api_key=filesystem_manager.load_secret_key(),
    )

    model = HERMES_405B

    concrete_involve_player_in_dialogue_strategy = ConcreteInvolvePlayerInDialogueStrategy(client, playthrough_name,
                                                                                           participants,
                                                                                           player_identifier)

    console_dialogue_observer = ConsoleDialogueObserver()

    concrete_involve_player_in_dialogue_strategy.attach(console_dialogue_observer)

    concrete_dialogue_factory = ConcreteDialogueFactory(client, model, playthrough_name, participants,
                                                        player_identifier, concrete_involve_player_in_dialogue_strategy)

    concrete_dialogue_factory.attach(console_dialogue_observer)

    dialogue_product = concrete_dialogue_factory.create_dialogue()

    SummarizeDialogueCommand(playthrough_name, client, HERMES_405B, participants, dialogue_product.get()).execute()

    StoreDialoguesCommand(playthrough_name, participants, dialogue_product.get()).execute()


if __name__ == "__main__":
    main()
