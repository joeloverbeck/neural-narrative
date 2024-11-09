from typing import Optional

from pydantic import BaseModel

from src.base.playthrough_manager import PlaythroughManager
from src.filesystem.path_manager import PathManager
from src.movements.configs.travel_narration_factory_config import (
    TravelNarrationFactoryConfig,
)
from src.movements.configs.travel_narration_factory_factories_config import (
    TravelNarrationFactoryFactoriesConfig,
)
from src.movements.products.travel_product import TravelProduct
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider
from src.time.time_manager import TimeManager


class TravelNarrationFactory(BaseToolResponseProvider):
    """
    Factory class to generate travel narration using LLMs.
    """

    def __init__(
        self,
        config: TravelNarrationFactoryConfig,
        factories_config: TravelNarrationFactoryFactoriesConfig,
        time_manager: Optional[TimeManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(
            factories_config.produce_tool_response_strategy_factory,
            path_manager,
        )

        self._config = config
        self._factories_config = factories_config

        self._time_manager = time_manager or TimeManager(self._config.playthrough_name)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._config.playthrough_name
        )

    def get_prompt_file(self) -> str:
        return self._path_manager.get_travel_narration_prompt_path()

    def get_prompt_kwargs(self) -> dict:
        current_place_identifier = (
            self._playthrough_manager.get_current_place_identifier()
        )
        current_place_data = self._factories_config.get_place_full_data_algorithm_factory.create_algorithm(
            current_place_identifier
        ).do_algorithm()
        destination_place_data = self._factories_config.get_place_full_data_algorithm_factory.create_algorithm(
            self._config.destination_identifier
        ).do_algorithm()

        player_name = self._factories_config.character_factory.create_character(
            self._playthrough_manager.get_player_identifier()
        ).name

        prompt_data = {
            "travel_context": self._config.travel_context,
            "time_of_day": self._time_manager.get_time_of_the_day(),
            "origin_area_template": self._factories_config.map_manager_factory.create_map_manager().get_current_place_template(),
            "origin_area_description": current_place_data["area_data"]["description"],
            "destination_area_template": destination_place_data["area_data"]["name"],
            "destination_area_description": destination_place_data["area_data"][
                "description"
            ],
            "player_and_followers_information": self._factories_config.player_and_followers_information_factory.get_information(),
            "player_name": player_name,
        }

        return prompt_data

    def get_user_content(self) -> str:
        return "Write the narration of the travel from the origin area to the destination area, filtered through the first-person perspective of the player, as per the above instructions."

    def create_product_from_base_model(self, response_model: BaseModel):
        return TravelProduct(
            narrative=response_model.narrative,
            outcome=response_model.outcome,
            is_valid=True,
        )
