import logging
from typing import Optional

from pydantic import BaseModel

from src.base.constants import (
    PLOT_BLUEPRINTS_GENERATION_PROMPT_FILE,
)
from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.concepts.models.plot_blueprint import PlotBlueprint
from src.concepts.products.plot_blueprints_product import PlotBlueprintsProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.factories.base_model_produce_tool_response_strategy_factory import (
    BaseModelProduceToolResponseStrategyFactory,
)

logger = logging.getLogger(__name__)


class PlotBlueprintsFactory(BaseConceptFactory):

    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: BaseModelProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsProvider,
        player_and_followers_information_factory: PlayerAndFollowersInformationFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(
            playthrough_name,
            produce_tool_response_strategy_factory,
            places_descriptions_factory,
            player_and_followers_information_factory,
            base_model=PlotBlueprint,
            prompt_file=PLOT_BLUEPRINTS_GENERATION_PROMPT_FILE,
            user_content="Generate a magnificent plot blueprint for a full story. Follow the provided instructions.",
            filesystem_manager=filesystem_manager,
        )

    def create_product_from_base_model(self, base_model: BaseModel):
        plot_blueprint = (
            str(base_model.plot_blueprint).replace("\n\n", " ").replace("\n", " ")
        )
        if not plot_blueprint.strip():
            return PlotBlueprintsProduct(
                None,
                is_valid=False,
                error="The LLM failed to produce a plot blueprint.",
            )
        return PlotBlueprintsProduct([plot_blueprint], is_valid=True)
