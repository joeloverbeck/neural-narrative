from typing import Optional

from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.constants import (
    INTERESTING_DILEMMAS_GENERATION_PROMPT_FILE,
    INTERESTING_DILEMMAS_GENERATION_TOOL_FILE,
)
from src.events.products.interesting_dilemmas_product import InterestingDilemmasProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class InterestingDilemmasFactory(BaseToolResponseProvider):
    def __init__(
        self,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        places_descriptions_for_prompt_factory: PlaceDescriptionsForPromptFactory,
        party_data_for_prompt_factory: PartyDataForPromptFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._places_descriptions_for_prompt_factory = (
            places_descriptions_for_prompt_factory
        )
        self._party_data_for_prompt_factory = party_data_for_prompt_factory

    def get_prompt_file(self) -> str:
        return INTERESTING_DILEMMAS_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:

        prompt_data = (
            self._places_descriptions_for_prompt_factory.create_place_descriptions_for_prompt()
        )

        prompt_data.update(
            self._party_data_for_prompt_factory.get_party_data_for_prompt()
        )

        return prompt_data

    def get_tool_file(self) -> str:
        return INTERESTING_DILEMMAS_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return (
            "Write a list of at least five intriguing moral and ethical dilemmas that "
            "could stem from the provided information, as per the above instructions."
        )

    def create_product(self, arguments: dict):
        return InterestingDilemmasProduct(
            [
                arguments.get("interesting_dilemma_1"),
                arguments.get("interesting_dilemma_2"),
                arguments.get("interesting_dilemma_3"),
                arguments.get("interesting_dilemma_4"),
                arguments.get("interesting_dilemma_5"),
            ],
            is_valid=True,
        )
