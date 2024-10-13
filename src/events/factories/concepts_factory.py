from typing import Optional

from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.constants import CONCEPTS_GENERATION_TOOL_FILE, CONCEPTS_GENERATION_PROMPT_FILE
from src.events.products.concepts_product import ConceptsProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class ConceptsFactory(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsFactory,
        player_and_followers_information_factory: PlayerAndFollowersInformationFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._places_descriptions_factory = places_descriptions_factory
        self._player_and_followers_information_factory = (
            player_and_followers_information_factory
        )

    def get_tool_file(self) -> str:
        return CONCEPTS_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return "Generate a magnificent concept for a full story. Follow the provided instructions."

    def create_product(self, arguments: dict):
        return ConceptsProduct(
            [
                arguments.get("concept"),
            ],
            is_valid=True,
        )

    def get_prompt_file(self) -> Optional[str]:
        return CONCEPTS_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        prompt_data = {
            "places_descriptions": self._places_descriptions_factory.get_information()
        }

        prompt_data.update(
            {
                "player_and_followers_information": self._player_and_followers_information_factory.get_information()
            }
        )

        return prompt_data
