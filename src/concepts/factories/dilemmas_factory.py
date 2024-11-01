from typing import Optional

from pydantic import BaseModel

from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.concepts.products.dilemmas_product import (
    DilemmasProduct,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.factories.base_model_produce_tool_response_strategy_factory import (
    BaseModelProduceToolResponseStrategyFactory,
)


class DilemmasFactory(BaseConceptFactory):

    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: BaseModelProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsProvider,
        player_and_followers_information_factory: RelevantCharactersInformationFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(
            playthrough_name,
            produce_tool_response_strategy_factory,
            places_descriptions_factory,
            player_and_followers_information_factory,
            prompt_file=self._path_manager.get_dilemmas_generation_prompt_path(),
            user_content="Write a list of three intriguing moral and ethical dilemmas that could stem from the provided information, as per the above instructions.",
            filesystem_manager=filesystem_manager,
        )

    def create_product_from_base_model(self, response_model: BaseModel):
        return DilemmasProduct(response_model.dilemmas, is_valid=True)
