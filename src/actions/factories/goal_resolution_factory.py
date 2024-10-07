from typing import Optional

from src.actions.products.goal_resolution_product import GoalResolutionProduct
from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.constants import (
    GOAL_RESOLUTION_GENERATION_TOOL_FILE,
    GOAL_RESOLUTION_GENERATION_PROMPT_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider
from src.time.time_manager import TimeManager


class GoalResolutionFactory(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: str,
        goal: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        party_data_for_prompt_factory: PartyDataForPromptFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
        time_manager: Optional[TimeManager] = None,
        map_manager: Optional[MapManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._playthrough_name = playthrough_name
        self._goal = goal
        self._party_data_for_prompt_factory = party_data_for_prompt_factory

        self._time_manager = time_manager or TimeManager(self._playthrough_name)
        self._map_manager = map_manager or MapManager(self._playthrough_name)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def get_tool_file(self) -> str:
        return GOAL_RESOLUTION_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return "Write a compelling and vivid narration, in third-person and past tense, of how the characters attempt to achieve the given goal. Follow the provided instructions."

    def create_product(self, arguments: dict):
        return GoalResolutionProduct(
            arguments.get("narration"),
            arguments.get("success_determination"),
            arguments.get("resolution"),
            is_valid=True,
        )

    def get_prompt_kwargs(self) -> dict:
        prompt_data = {
            "goal": self._goal,
            "hour": self._time_manager.get_hour(),
            "time_of_day": self._time_manager.get_time_of_the_day(),
            "place_description": self._map_manager.get_place_description(
                self._playthrough_manager.get_current_place_identifier()
            ),
        }

        party_data = self._party_data_for_prompt_factory.get_party_data_for_prompt()

        prompt_data.update(party_data)

        return prompt_data

    def get_prompt_file(self) -> Optional[str]:
        return GOAL_RESOLUTION_GENERATION_PROMPT_FILE
