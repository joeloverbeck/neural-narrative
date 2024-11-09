from typing import Optional

from pydantic import BaseModel

from src.base.products.texts_product import TextsProduct
from src.base.validators import validate_non_empty_string
from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.filesystem.path_manager import PathManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.factories.base_model_produce_tool_response_strategy_factory import (
    BaseModelProduceToolResponseStrategyFactory,
)


class AntagonistsFactory(BaseConceptFactory):

    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: BaseModelProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsProvider,
        player_and_followers_information_factory: RelevantCharactersInformationFactory,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        path_manager = path_manager or PathManager()

        super().__init__(
            playthrough_name,
            produce_tool_response_strategy_factory,
            places_descriptions_factory,
            player_and_followers_information_factory,
            prompt_file=path_manager.get_antagonists_generation_prompt_path(),
            user_content="Generate a complex and intriguing antagonist profile that could stem from the provided information, as per the above instructions.",
            path_manager=path_manager,
        )

    def create_product_from_base_model(self, response_model: BaseModel):
        antagonist = str(response_model.antagonist)

        return TextsProduct([antagonist.replace("\n\n", "\n")], is_valid=True)
