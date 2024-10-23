from typing import Optional

from src.actions.products.action_resolution_product import ActionResolutionProduct
from src.base.validators import validate_non_empty_string
from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider
from src.time.time_manager import TimeManager


class ActionResolutionFactory(BaseToolResponseProvider):

    def __init__(
        self,
        playthrough_name: str,
        action_name: str,
        action_goal: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsProvider,
        players_and_followers_information_factory: PlayerAndFollowersInformationFactory,
        prompt_file: str,
        tool_file: str,
        filesystem_manager: Optional[FilesystemManager] = None,
        time_manager: Optional[TimeManager] = None,
    ):
        validate_non_empty_string(action_name, "action_name")
        validate_non_empty_string(action_goal, "action_goal")

        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)
        self._playthrough_name = playthrough_name
        self._action_name = action_name
        self._action_goal = action_goal
        self._places_descriptions_factory = places_descriptions_factory
        self._players_and_followers_information_factory = (
            players_and_followers_information_factory
        )
        self._prompt_file = prompt_file
        self._tool_file = tool_file

        self._time_manager = time_manager or TimeManager(self._playthrough_name)

    def get_prompt_file(self) -> str:
        return self._prompt_file

    def get_prompt_kwargs(self) -> dict:
        prompt_data = {
            "hour": self._time_manager.get_hour(),
            "time_of_day": self._time_manager.get_time_of_the_day(),
            "facts_known": self._filesystem_manager.read_file(
                self._filesystem_manager.get_file_path_to_facts(self._playthrough_name)
            ),
        }
        prompt_data.update(
            {"places_descriptions": self._places_descriptions_factory.get_information()}
        )
        prompt_data.update(
            {
                "player_and_followers_information": self._players_and_followers_information_factory.get_information()
            }
        )
        return prompt_data

    def _get_tool_data(self) -> dict:
        return self._filesystem_manager.load_existing_or_new_json_file(self._tool_file)

    def get_user_content(self) -> str:
        return f"Generate a detailed narrative describing the player's attempt at a {self._action_name} action within a rich, immersive world. Use the provided information about the player, their followers, the world's conditions, and the specific locations involved. {self._action_name} goal: {self._action_goal}"

    def create_product_from_dict(self, arguments: dict):
        return ActionResolutionProduct(
            arguments.get("narrative"), arguments.get("outcome"), is_valid=True
        )
