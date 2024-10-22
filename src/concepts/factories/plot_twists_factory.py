import logging
from typing import Optional
from src.base.constants import PLOT_TWISTS_GENERATION_TOOL_FILE, PLOT_TWISTS_GENERATION_PROMPT_FILE
from src.characters.factories.player_and_followers_information_factory import PlayerAndFollowersInformationFactory
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.concepts.products.plot_twists_product import PlotTwistsProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.factories.produce_tool_response_strategy_factory import ProduceToolResponseStrategyFactory
logger = logging.getLogger(__name__)


class PlotTwistsFactory(BaseConceptFactory):

    def __init__(self, playthrough_name: str,
                 produce_tool_response_strategy_factory:
                 ProduceToolResponseStrategyFactory, places_descriptions_factory:
            PlacesDescriptionsProvider,
                 player_and_followers_information_factory:
                 PlayerAndFollowersInformationFactory, filesystem_manager: Optional[
                FilesystemManager] = None):
        super().__init__(playthrough_name,
            produce_tool_response_strategy_factory,
            places_descriptions_factory,
                         player_and_followers_information_factory, tool_file=
                         PLOT_TWISTS_GENERATION_TOOL_FILE, prompt_file=
                         PLOT_TWISTS_GENERATION_PROMPT_FILE, user_content=
                         'Generate three captivating plot twists that could dramatically alter the storyline. Follow the provided instructions.'
                         , filesystem_manager=filesystem_manager)

    def create_product(self, arguments: dict):
        plot_twists = []
        for i in range(1, 4):
            key = f'plot_twist_{i}'
            twist = arguments.get(key)
            if not twist:
                raise ValueError(f"LLM didn't produce plot twist {key}.")
            plot_twists.append(twist)
        return PlotTwistsProduct(plot_twists, is_valid=True)
