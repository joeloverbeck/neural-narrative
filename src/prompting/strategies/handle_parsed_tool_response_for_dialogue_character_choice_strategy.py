from src.base.playthrough_manager import PlaythroughManager
from src.base.required_string import RequiredString
from src.dialogues.participants import Participants
from src.dialogues.strategies.prevent_llm_from_choosing_player_as_next_speaker_strategy import (
    PreventLlmFromChoosingPlayerAsNextSpeakerStrategy,
)
from src.prompting.abstracts.factory_products import (
    LlmToolResponseProduct,
    LlmContentProduct,
)
from src.prompting.factories.tool_response_parsing_provider_factory import (
    ToolResponseParsingProviderFactory,
)
from src.prompting.products.concrete_llm_tool_response_product import (
    ConcreteLlmToolResponseProduct,
)


class HandleParsedToolResponseForDialogueCharacterChoiceStrategy:
    def __init__(
        self,
            playthrough_name: RequiredString,
        participants: Participants,
        tool_response_parsing_provider_factory: ToolResponseParsingProviderFactory,
        prevent_llm_from_choosing_player_as_next_speaker_strategy: PreventLlmFromChoosingPlayerAsNextSpeakerStrategy,
        playthrough_manager: PlaythroughManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")
        if participants is None:
            raise ValueError("participants must not be None.")
        if tool_response_parsing_provider_factory is None:
            raise ValueError("tool_response_parsing_provider_factory must not be None.")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._tool_response_parsing_provider_factory = (
            tool_response_parsing_provider_factory
        )
        self._prevent_llm_from_choosing_player_as_next_speaker_strategy = (
            prevent_llm_from_choosing_player_as_next_speaker_strategy
        )

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def handle_parsed_tool_response(
        self, llm_content_product: LlmContentProduct
    ) -> LlmToolResponseProduct:
        """
        Handles the parsed tool response from the LLM, ensuring the next speaker is not the player.

        :param llm_content_product: The LLM content product to handle.
        :return: An LlmToolResponseProduct indicating the result.
        """
        tool_response_parsing_product = self._tool_response_parsing_provider_factory.create_tool_response_parsing_provider(
            llm_content_product
        ).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            return ConcreteLlmToolResponseProduct(
                tool_response_parsing_product.get(),
                is_valid=False,
                error=f"Unable to parse the tool response from the LLM: {tool_response_parsing_product.get_error()}",
            )

        function_call_arguments = tool_response_parsing_product.get()["arguments"]

        if "identifier" not in function_call_arguments:
            return ConcreteLlmToolResponseProduct(
                tool_response_parsing_product.get(),
                is_valid=False,
                error=f"The LLM didn't provide the identifier of the next speaker: {tool_response_parsing_product.get()}",
            )

        # We have the chance here to intercept the character turn choice in case the AI idiotically chose to speak as the player.
        function_call_arguments = self._prevent_llm_from_choosing_player_as_next_speaker_strategy.prevent_llm_from_choosing_player(
            function_call_arguments
        )

        return ConcreteLlmToolResponseProduct(function_call_arguments, is_valid=True)
