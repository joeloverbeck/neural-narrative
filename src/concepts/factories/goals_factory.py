# src/concepts/factories/goals_factory.py

import logging
from typing import Optional

from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.concepts.products.goals_product import GoalsProduct
from src.constants import GOALS_GENERATION_TOOL_FILE, GOALS_GENERATION_PROMPT_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.playthrough_name import PlaythroughName
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)

logger = logging.getLogger(__name__)


class GoalsFactory(BaseConceptFactory):
    def __init__(
        self,
        playthrough_name: PlaythroughName,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsFactory,
        player_and_followers_information_factory: PlayerAndFollowersInformationFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(
            playthrough_name,
            produce_tool_response_strategy_factory,
            places_descriptions_factory,
            player_and_followers_information_factory,
            tool_file=GOALS_GENERATION_TOOL_FILE,
            prompt_file=GOALS_GENERATION_PROMPT_FILE,
            user_content="Generate three intriguing and engaging short-term goals for the player to pursue. Follow the provided instructions.",
            filesystem_manager=filesystem_manager,
        )

    def create_product(self, arguments: dict):
        goals = []
        for i in range(1, 4):
            key = f"goal_{i}"
            goal = arguments.get(key)
            if not goal:
                logger.warning(f"LLM didn't produce {key}")
            goals.append(goal)
        return GoalsProduct(goals, is_valid=True)
