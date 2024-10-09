from typing import Optional

from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.constants import CONCEPTS_GENERATION_TOOL_FILE, CONCEPTS_GENERATION_PROMPT_FILE
from src.events.products.concepts_product import ConceptsProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class ConceptsFactory(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        place_descriptions_for_prompt_factory: PlaceDescriptionsForPromptFactory,
        party_data_for_prompty_factory: PartyDataForPromptFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._place_descriptions_for_prompt_factory = (
            place_descriptions_for_prompt_factory
        )
        self._party_data_for_prompt_factory = party_data_for_prompty_factory

    def get_tool_file(self) -> str:
        return CONCEPTS_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return "Generate five magnificent concepts for full stories. Follow the provided instructions."

    def create_product(self, arguments: dict):
        return ConceptsProduct(
            [
                arguments.get("concept_1"),
                arguments.get("concept_2"),
                arguments.get("concept_3"),
                arguments.get("concept_4"),
                arguments.get("concept_5"),
            ],
            is_valid=True,
        )

    def get_prompt_file(self) -> Optional[str]:
        return CONCEPTS_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        prompt_data = (
            self._place_descriptions_for_prompt_factory.create_place_descriptions_for_prompt()
        )

        prompt_data.update(
            self._party_data_for_prompt_factory.get_party_data_for_prompt()
        )

        return prompt_data
