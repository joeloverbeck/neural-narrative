from pathlib import Path
from typing import Optional

from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)
from src.concepts.concepts_manager import ConceptsManager
from src.filesystem.path_manager import PathManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class BaseConceptFactory(BaseToolResponseProvider):

    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsProvider,
        player_and_followers_information_factory: RelevantCharactersInformationFactory,
        prompt_file: Path,
        user_content: str,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        self._playthrough_name = playthrough_name
        self._places_descriptions_factory = places_descriptions_factory
        self._player_and_followers_information_factory = (
            player_and_followers_information_factory
        )
        self._prompt_file = prompt_file
        self._user_content = user_content

    def get_user_content(self) -> str:
        return self._user_content

    def get_prompt_file(self) -> Optional[Path]:
        return self._prompt_file

    def get_prompt_kwargs(self) -> dict:
        return ConceptsManager(self._playthrough_name).get_prompt_data(
            self._places_descriptions_factory,
            self._player_and_followers_information_factory,
        )
