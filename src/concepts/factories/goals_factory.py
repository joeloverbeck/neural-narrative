import logging
from typing import Optional

from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.concepts.plot_blueprints_manager import PlotBlueprintsManager
from src.concepts.products.goals_product import GoalsProduct
from src.constants import GOALS_GENERATION_TOOL_FILE, GOALS_GENERATION_PROMPT_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.playthrough_name import PlaythroughName
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
        places_descriptions_factory: PlacesDescriptionsFactory,
        player_and_followers_information_factory: PlayerAndFollowersInformationFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._playthrough_name = playthrough_name
        self._places_descriptions_factory = places_descriptions_factory
        self._player_and_followers_information_factory = (
            player_and_followers_information_factory
        )

    def get_tool_file(self) -> str:
        return GOALS_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return "Generate three intriguing and engaging short-term goals for the player to pursue. Follow the provided instructions."

    def create_product(self, arguments: dict):
        # if it turns out that it has failed to produce goals, at least log it.
        if not arguments.get("goal_1"):
            logger.warning("LLM didn't produce goal_1")
        if not arguments.get("goal_2"):
            logger.warning("LLM didn't produce goal_2")
        if not arguments.get("goal_3"):
            logger.warning("LLM didn't produce goal_3")

        return GoalsProduct(
            [arguments.get("goal_1"), arguments.get("goal_2"), arguments.get("goal_3")],
            is_valid=True,
        )

    def get_prompt_file(self) -> Optional[str]:
        return GOALS_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        return PlotBlueprintsManager(
            PlaythroughName(self._playthrough_name)
        ).get_prompt_data(
            self._places_descriptions_factory,
            self._player_and_followers_information_factory,
        )
