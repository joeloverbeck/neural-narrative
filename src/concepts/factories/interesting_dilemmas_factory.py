from typing import Optional

from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.concepts.concepts_manager import ConceptsManager
from src.concepts.products.interesting_dilemmas_product import (
    InterestingDilemmasProduct,
)
from src.constants import (
    INTERESTING_DILEMMAS_GENERATION_PROMPT_FILE,
    INTERESTING_DILEMMAS_GENERATION_TOOL_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.playthrough_name import PlaythroughName
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class InterestingDilemmasFactory(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: PlaythroughName,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsFactory,
        player_and_followers_information_factory: PlayerAndFollowersInformationFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._playthrough_name = playthrough_name
        self._places_descriptions_factory = places_descriptions_factory
        self._player_and_followers_information_factory = (
            player_and_followers_information_factory
        )

    def get_prompt_file(self) -> str:
        return INTERESTING_DILEMMAS_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        return ConceptsManager(self._playthrough_name).get_prompt_data(
            self._places_descriptions_factory,
            self._player_and_followers_information_factory,
        )

    def get_tool_file(self) -> str:
        return INTERESTING_DILEMMAS_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return (
            "Write a list three intriguing moral and ethical dilemmas that "
            "could stem from the provided information, as per the above instructions."
        )

    def create_product(self, arguments: dict):
        return InterestingDilemmasProduct(
            [
                arguments.get("interesting_dilemma_1"),
                arguments.get("interesting_dilemma_2"),
                arguments.get("interesting_dilemma_3"),
            ],
            is_valid=True,
        )
