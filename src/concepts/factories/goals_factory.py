import logging
from typing import Optional

from pydantic import BaseModel

from src.base.constants import GOALS_GENERATION_PROMPT_FILE
from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.concepts.models.goals import Goals
from src.concepts.products.goals_product import GoalsProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.factories.base_model_produce_tool_response_strategy_factory import (
    BaseModelProduceToolResponseStrategyFactory,
)

logger = logging.getLogger(__name__)


class GoalsFactory(BaseConceptFactory):

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
            base_model=Goals,
            prompt_file=GOALS_GENERATION_PROMPT_FILE,
            user_content="Generate three intriguing and engaging short-term goals for the player to pursue. Follow the provided instructions.",
            filesystem_manager=filesystem_manager,
        )

    def create_product_from_base_model(self, base_model: BaseModel):
        return GoalsProduct(base_model.goals, is_valid=True)
