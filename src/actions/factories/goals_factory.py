import logging
from typing import Optional

from src.actions.products.goals_product import GoalsProduct
from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.constants import GOALS_GENERATION_TOOL_FILE, GOALS_GENERATION_PROMPT_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider

logger = logging.getLogger(__name__)


class GoalsFactory(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        place_descriptions_for_prompt_factory: PlaceDescriptionsForPromptFactory,
        party_data_for_prompt_factory: PartyDataForPromptFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._playthrough_name = playthrough_name
        self._place_descriptions_for_prompt_factory = (
            place_descriptions_for_prompt_factory
        )
        self._party_data_for_prompt_factory = party_data_for_prompt_factory

    def get_tool_file(self) -> str:
        return GOALS_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return "Generate a list of five intriguing and engaging short-term goals for the player to pursue. Follow the provided instructions."

    def create_product(self, arguments: dict):
        # if it turns out that it has failed to produce goals, at least log it.
        if not arguments.get("goal_1"):
            logger.warning("LLM didn't produce goal_1")
        if not arguments.get("goal_2"):
            logger.warning("LLM didn't produce goal_2")
        if not arguments.get("goal_3"):
            logger.warning("LLM didn't produce goal_3")
        if not arguments.get("goal_4"):
            logger.warning("LLM didn't produce goal_4")
        if not arguments.get("goal_5"):
            logger.warning("LLM didn't produce goal_5")

        return GoalsProduct(
            [
                arguments.get("goal_1"),
                arguments.get("goal_2"),
                arguments.get("goal_3"),
                arguments.get("goal_4"),
                arguments.get("goal_5"),
            ],
            is_valid=True,
        )

    def get_prompt_file(self) -> Optional[str]:
        return GOALS_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        prompt_data = (
            self._place_descriptions_for_prompt_factory.create_place_descriptions_for_prompt()
        )

        prompt_data.update(
            self._party_data_for_prompt_factory.get_party_data_for_prompt()
        )

        return prompt_data
