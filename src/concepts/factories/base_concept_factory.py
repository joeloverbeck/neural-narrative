# src/concepts/factories/base_concept_factory.py

from typing import Optional

from src.base.required_string import RequiredString
from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.concepts.concepts_manager import ConceptsManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class BaseConceptFactory(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: RequiredString,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
            places_descriptions_factory: PlacesDescriptionsProvider,
        player_and_followers_information_factory: PlayerAndFollowersInformationFactory,
            tool_file: RequiredString,
            prompt_file: RequiredString,
            user_content: RequiredString,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._playthrough_name = playthrough_name
        self._places_descriptions_factory = places_descriptions_factory
        self._player_and_followers_information_factory = (
            player_and_followers_information_factory
        )
        self._tool_file = tool_file
        self._prompt_file = prompt_file
        self._user_content = user_content

    def get_tool_file(self) -> RequiredString:
        return self._tool_file

    def get_user_content(self) -> RequiredString:
        return self._user_content

    def get_prompt_file(self) -> Optional[RequiredString]:
        return self._prompt_file

    def get_prompt_kwargs(self) -> dict:
        return ConceptsManager(self._playthrough_name).get_prompt_data(
            self._places_descriptions_factory,
            self._player_and_followers_information_factory,
        )

    def create_product(self, arguments: dict):
        raise NotImplementedError("Subclasses must implement create_product.")
