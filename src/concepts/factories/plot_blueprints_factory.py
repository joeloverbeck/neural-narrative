# src/concepts/factories/plot_blueprints_factory.py

from typing import Optional

from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.concepts.products.plot_blueprints_product import PlotBlueprintsProduct
from src.constants import (
    PLOT_BLUEPRINTS_GENERATION_TOOL_FILE,
    PLOT_BLUEPRINTS_GENERATION_PROMPT_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.playthrough_name import PlaythroughName
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class PlotBlueprintsFactory(BaseConceptFactory):
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
            tool_file=PLOT_BLUEPRINTS_GENERATION_TOOL_FILE,
            prompt_file=PLOT_BLUEPRINTS_GENERATION_PROMPT_FILE,
            user_content="Generate a magnificent plot blueprint for a full story. Follow the provided instructions.",
            filesystem_manager=filesystem_manager,
        )

    def create_product(self, arguments: dict):
        plot_blueprint = arguments.get("plot_blueprint")
        if not plot_blueprint:
            return PlotBlueprintsProduct(
                None,
                is_valid=False,
                error="The LLM failed to produce a plot blueprint.",
            )
        return PlotBlueprintsProduct([plot_blueprint], is_valid=True)
