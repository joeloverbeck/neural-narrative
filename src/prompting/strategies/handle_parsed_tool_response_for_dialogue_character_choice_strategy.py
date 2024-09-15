import random

from src.dialogues.participants import Participants
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.factory_products import LlmToolResponseProduct, LlmContentProduct
from src.prompting.factories.tool_response_parsing_provider_factory import ToolResponseParsingProviderFactory
from src.prompting.products.concrete_llm_tool_response_product import ConcreteLlmToolResponseProduct


class HandleParsedToolResponseForDialogueCharacterChoiceStrategy:
    def __init__(self, playthrough_name: str, participants: Participants,
                 tool_response_parsing_provider_factory: ToolResponseParsingProviderFactory,
                 filesystem_manager: FilesystemManager = None):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._tool_response_parsing_provider_factory = tool_response_parsing_provider_factory

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def handle_parsed_tool_response(self, llm_content_product: LlmContentProduct) -> LlmToolResponseProduct:
        tool_response_parsing_product = self._tool_response_parsing_provider_factory.create_tool_response_parsing_provider(
            llm_content_product).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            return ConcreteLlmToolResponseProduct(tool_response_parsing_product.get(), is_valid=False,
                                                  error=f"Was unable to parse the tool response from the LLM: {tool_response_parsing_product.get_error()}")

        function_call_arguments = tool_response_parsing_product.get()["arguments"]

        if "identifier" not in function_call_arguments:
            return ConcreteLlmToolResponseProduct(tool_response_parsing_product.get(), is_valid=False,
                                                  error=f"The LLM didn't produce the identifier of the character who ought to speak next: {tool_response_parsing_product.get()}")

        # We have the chance here to intercept the character turn choice in case the AI idiotically chose to speak as the player.
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(self._playthrough_name))

        if playthrough_metadata["player_identifier"] == function_call_arguments["identifier"]:
            # Change the "identifier" in function_call_arguments to any random participant in self._participants.get() that isn't the player.
            participant_keys = self._participants.get_participant_keys()

            # Remove the player's identifier from the participant keys
            participant_keys.remove(playthrough_metadata["player_identifier"])

            if participant_keys:
                # Select a random participant that is not the player
                function_call_arguments["identifier"] = random.choice(participant_keys)
            else:
                return ConcreteLlmToolResponseProduct(tool_response_parsing_product.get(), is_valid=False,
                                                      error="No other participants available besides the player.")

        return ConcreteLlmToolResponseProduct(function_call_arguments, is_valid=True)
