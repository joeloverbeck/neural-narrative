# src/concepts/factories/plot_twists_factory.py

import logging
from typing import Optional

from src.base.constants import (
    PLOT_TWISTS_GENERATION_TOOL_FILE,
    PLOT_TWISTS_GENERATION_PROMPT_FILE,
)
from src.base.playthrough_name import RequiredString
from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.concepts.products.plot_twists_product import PlotTwistsProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)

logger = logging.getLogger(__name__)


class PlotTwistsFactory(BaseConceptFactory):
    def __init__(
        self,
        playthrough_name: RequiredString,
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
            tool_file=PLOT_TWISTS_GENERATION_TOOL_FILE,
            prompt_file=PLOT_TWISTS_GENERATION_PROMPT_FILE,
            user_content="Generate three captivating plot twists that could dramatically alter the storyline. Follow the provided instructions.",
            filesystem_manager=filesystem_manager,
        )

    def create_product(self, arguments: dict):
        plot_twists = []
        for i in range(1, 4):
            key = f"plot_twist_{i}"
            twist = arguments.get(key)
            if not twist:
                logger.warning(f"LLM didn't produce {key}")
            plot_twists.append(twist)
        return PlotTwistsProduct(plot_twists, is_valid=True)
