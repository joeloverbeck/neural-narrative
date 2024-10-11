from typing import Optional

from src.actions.products.action_resolution_product import ActionResolutionProduct
from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.constants import (
    INVESTIGATE_RESOLUTION_GENERATION_PROMPT_FILE,
    INVESTIGATE_RESOLUTION_GENERATION_TOOL_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider
from src.time.time_manager import TimeManager


class InvestigateResolutionFactory(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: str,
        investigation_goal: str,
        facts_already_known: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        place_descriptions_for_prompt_factory: PlaceDescriptionsForPromptFactory,
        party_data_for_prompt_factory: PartyDataForPromptFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
        time_manager: Optional[TimeManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not investigation_goal:
            raise ValueError("investigation_goal can't be empty.")

        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._playthrough_name = playthrough_name
        self._investigation_goal = investigation_goal
        self._facts_already_known = facts_already_known

        self._place_descriptions_for_prompt_factory = (
            place_descriptions_for_prompt_factory
        )
        self._party_data_for_prompt_factory = party_data_for_prompt_factory

        self._time_manager = time_manager or TimeManager(self._playthrough_name)

    def get_prompt_file(self) -> str:
        return INVESTIGATE_RESOLUTION_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        prompt_data = {
            "hour": self._time_manager.get_hour(),
            "time_of_day": self._time_manager.get_time_of_the_day(),
            "investigation_goal": self._investigation_goal,
            "facts_already_known": self._facts_already_known,
        }

        prompt_data.update(
            self._place_descriptions_for_prompt_factory.create_place_descriptions_for_prompt()
        )

        prompt_data.update(
            self._party_data_for_prompt_factory.get_party_data_for_prompt()
        )

        return prompt_data

    def get_tool_file(self) -> str:
        return INVESTIGATE_RESOLUTION_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return (
            "Generate a detailed narrative describing the player's attempt at an Investigate action within a rich,"
            "immersive world. Use the provided information about the player, their followers, the world's conditions, and the specific locations involved."
        )

    def create_product(self, arguments: dict):
        print(arguments)
        return ActionResolutionProduct(
            arguments.get("narrative"),
            arguments.get("outcome"),
            is_valid=True,
        )