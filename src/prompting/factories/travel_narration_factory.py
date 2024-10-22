from typing import Optional
from src.base.constants import TRAVEL_NARRATION_PROMPT_FILE, TRAVEL_NARRATION_TOOL_FILE
from src.base.playthrough_manager import PlaythroughManager
from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.products.travel_narration_product import TravelNarrationProduct
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class TravelNarrationFactory(BaseToolResponseProvider):
    """
    Factory class to generate travel narration using LLMs.
    """

    def __init__(
        self,
        playthrough_name: str,
        destination_identifier: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        player_and_followers_information_factory: PlayerAndFollowersInformationFactory,
        map_manager_factory: MapManagerFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)
        self._destination_identifier = destination_identifier
        self._player_and_followers_information_factory = (
            player_and_followers_information_factory
        )
        self._map_manager_factory = map_manager_factory
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )

    def get_prompt_file(self) -> str:
        return TRAVEL_NARRATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        current_place_identifier = (
            self._playthrough_manager.get_current_place_identifier()
        )
        current_place_data = (
            self._map_manager_factory.create_map_manager().get_place_full_data(
                current_place_identifier
            )
        )
        destination_place_data = (
            self._map_manager_factory.create_map_manager().get_place_full_data(
                self._destination_identifier
            )
        )
        prompt_data = {
            "origin_area_template": self._map_manager_factory.create_map_manager().get_current_place_template(),
            "origin_area_description": current_place_data["area_data"]["description"],
            "destination_area_template": destination_place_data["area_data"]["name"],
            "destination_area_description": destination_place_data["area_data"][
                "description"
            ],
        }
        prompt_data.update(
            {
                "player_and_followers_information": self._player_and_followers_information_factory.get_information()
            }
        )
        return prompt_data

    def get_tool_file(self) -> str:
        return TRAVEL_NARRATION_TOOL_FILE

    def get_user_content(self) -> str:
        return "Write the narration of the travel from the origin area to the destination area, filtered through the first-person perspective of the player, as per the above instructions."

    def create_product(self, arguments: dict):
        return TravelNarrationProduct(
            travel_narration=arguments.get("narration", "The travel was uneventful."),
            is_valid=True,
        )
