from typing import Optional

from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.constants import (
    INTERESTING_SITUATIONS_GENERATION_PROMPT_FILE,
    INTERESTING_SITUATIONS_GENERATION_TOOL_FILE,
)
from src.events.products.interesting_situations_product import (
    InterestingSituationsProduct,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class InterestingSituationsFactory(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        party_data_for_prompty_factory: PartyDataForPromptFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._playthrough_name = playthrough_name
        self._party_data_for_prompt_factory = party_data_for_prompty_factory

    def get_prompt_file(self) -> str:
        return INTERESTING_SITUATIONS_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        return self._party_data_for_prompt_factory.get_party_data_for_prompt()

    def get_tool_file(self) -> str:
        return INTERESTING_SITUATIONS_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return (
            "Write a list of at least five very interesting and intriguing situations "
            "that could stem from the information about the player, his possible followers, and the combined memories, as per the above instructions."
        )

    def create_product(self, arguments: dict):
        return InterestingSituationsProduct(
            arguments.get("interesting_situations"), is_valid=True
        )
