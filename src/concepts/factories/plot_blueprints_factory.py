import logging
from typing import Optional

from pydantic import BaseModel

from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.concepts.products.plot_blueprints_product import PlotBlueprintsProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.filesystem.path_manager import PathManager
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
        player_and_followers_information_factory: RelevantCharactersInformationFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        path_manager = path_manager or PathManager()

        super().__init__(
            playthrough_name,
            produce_tool_response_strategy_factory,
            places_descriptions_factory,
            player_and_followers_information_factory,
            prompt_file=path_manager.get_plot_blueprints_generation_prompt_path(),
            user_content="Generate a magnificent plot blueprint for a full story. Follow the provided instructions.",
            filesystem_manager=filesystem_manager,
            path_manager=path_manager,
        )

    def create_product_from_base_model(self, response_model: BaseModel):
        plot_blueprint = (
            str(response_model.plot_blueprint).replace("\n\n", " ").replace("\n", " ")
        )
        if not plot_blueprint.strip():
            return PlotBlueprintsProduct(
                None,
                is_valid=False,
                error="The LLM failed to produce a plot blueprint.",
            )
        return PlotBlueprintsProduct([plot_blueprint], is_valid=True)
