from typing import Optional
from src.base.constants import CONNECTION_GENERATION_PROMPT_FILE, CONNECTION_GENERATION_TOOL_FILE
from src.characters.character import Character
from src.characters.factories.character_information_provider_factory import CharacterInformationProviderFactory
from src.characters.products.connection_product import ConnectionProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.produce_tool_response_strategy_factory import ProduceToolResponseStrategyFactory
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class ConnectionFactory(BaseToolResponseProvider):

    def __init__(self, playthrough_name: str, character_a_identifier: str,
                 character_b_identifier: str, character_information_provider_factory:
            CharacterInformationProviderFactory,
                 produce_tool_response_strategy_factory:
                 ProduceToolResponseStrategyFactory, filesystem_manager: Optional[
                FilesystemManager] = None):
        super().__init__(produce_tool_response_strategy_factory,
                         filesystem_manager)
        self._character_information_provider_factory = (
            character_information_provider_factory)
        self._playthrough_name = playthrough_name
        self._character_a_identifier = character_a_identifier
        self._character_b_identifier = character_b_identifier

    def get_tool_file(self) -> str:
        return CONNECTION_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return (
            'Generate a meaningful and compelling connection between the two provided characters. Follow the instructions.'
        )

    def create_product(self, arguments: dict):
        if not arguments.get('connection'):
            return ConnectionProduct(None, is_valid=False, error=
            'The LLM failed to produce a connection.')
        return ConnectionProduct(arguments.get('connection'), is_valid=True)

    def get_prompt_file(self) -> Optional[str]:
        return CONNECTION_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        character_a_information = (self.
                                   _character_information_provider_factory.create_provider(self.
                                                                                           _character_a_identifier))
        character_b_information = (self.
                                   _character_information_provider_factory.create_provider(self.
                                                                                           _character_b_identifier))
        name_a = Character(self._playthrough_name, self._character_a_identifier
                           ).name
        name_b = Character(self._playthrough_name, self._character_b_identifier
                           ).name
        return {'character_a_information': character_a_information,
                'character_b_information': character_b_information, 'name_a':
                    name_a, 'name_b': name_b}
