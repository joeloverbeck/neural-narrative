from typing import Optional

from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.concepts.products.interesting_situations_product import (
    InterestingSituationsProduct,
)
from src.constants import (
    INTERESTING_SITUATIONS_GENERATION_PROMPT_FILE,
    INTERESTING_SITUATIONS_GENERATION_TOOL_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class InterestingSituationsFactory(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsFactory,
        player_and_followers_information_factory: PlayerAndFollowersInformationFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._playthrough_name = playthrough_name
        self._places_descriptions_factory = places_descriptions_factory
        self._player_and_followers_information_factory = (
            player_and_followers_information_factory
        )

    def get_prompt_file(self) -> str:
        return INTERESTING_SITUATIONS_GENERATION_PROMPT_FILE

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

    def get_tool_file(self) -> str:
        return INTERESTING_SITUATIONS_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return (
            "Write three very interesting and intriguing situations "
            "that could stem from the information about the player, his possible followers, and the combined memories, as per the above instructions."
        )

    def create_product(self, arguments: dict):
        return InterestingSituationsProduct(
            [
                arguments.get("interesting_situation_1"),
                arguments.get("interesting_situation_2"),
                arguments.get("interesting_situation_3"),
            ],
            is_valid=True,
        )
