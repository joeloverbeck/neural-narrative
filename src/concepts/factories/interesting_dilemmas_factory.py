from typing import Optional

from src.base.constants import (
    INTERESTING_DILEMMAS_GENERATION_PROMPT_FILE,
    INTERESTING_DILEMMAS_GENERATION_TOOL_FILE,
)
from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.concepts.products.interesting_dilemmas_product import (
    InterestingDilemmasProduct,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class InterestingDilemmasFactory(BaseConceptFactory):

    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsProvider,
        player_and_followers_information_factory: PlayerAndFollowersInformationFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(
            playthrough_name,
            produce_tool_response_strategy_factory,
            places_descriptions_factory,
            player_and_followers_information_factory,
            tool_file=INTERESTING_DILEMMAS_GENERATION_TOOL_FILE,
            prompt_file=INTERESTING_DILEMMAS_GENERATION_PROMPT_FILE,
            user_content="Write a list of three intriguing moral and ethical dilemmas that could stem from the provided information, as per the above instructions.",
            filesystem_manager=filesystem_manager,
        )

    def create_product(self, arguments: dict):
        dilemmas = []
        for i in range(1, 4):
            key = f"interesting_dilemma_{i}"
            dilemmas.append(arguments.get(key))
        return InterestingDilemmasProduct(dilemmas, is_valid=True)
