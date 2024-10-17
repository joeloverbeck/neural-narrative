# src/concepts/factories/interesting_situations_factory.py

from typing import Optional

from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.concepts.products.interesting_situations_product import (
    InterestingSituationsProduct,
)
from src.constants import (
    INTERESTING_SITUATIONS_GENERATION_PROMPT_FILE,
    INTERESTING_SITUATIONS_GENERATION_TOOL_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.playthrough_name import PlaythroughName
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class InterestingSituationsFactory(BaseConceptFactory):
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
            tool_file=INTERESTING_SITUATIONS_GENERATION_TOOL_FILE,
            prompt_file=INTERESTING_SITUATIONS_GENERATION_PROMPT_FILE,
            user_content=(
                "Write three very interesting and intriguing situations "
                "that could stem from the information about the player, his possible followers, and the combined memories, as per the above instructions."
            ),
            filesystem_manager=filesystem_manager,
        )

    def create_product(self, arguments: dict):
        situations = []
        for i in range(1, 4):
            key = f"interesting_situation_{i}"
            situations.append(arguments.get(key))
        return InterestingSituationsProduct(situations, is_valid=True)
