from typing import Optional

from pydantic import BaseModel

from src.base.tools import join_with_newline
from src.characters.configs.secrets_factory_config import SecretsFactoryConfig
from src.characters.configs.secrets_factory_factories_config import (
    SecretsFactoryFactoriesConfig,
)
from src.characters.products.secrets_product import SecretsProduct
from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.filesystem.path_manager import PathManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class SecretsFactory(BaseToolResponseProvider):

    def __init__(
        self,
        config: SecretsFactoryConfig,
        format_known_facts_algorithm: FormatKnownFactsAlgorithm,
        places_descriptions_provider: PlacesDescriptionsProvider,
        factories_config: SecretsFactoryFactoriesConfig,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(
            factories_config.produce_tool_response_strategy_factory, path_manager
        )

        self._config = config
        self._format_known_facts_algorithm = format_known_facts_algorithm
        self._places_descriptions_provider = places_descriptions_provider
        self._factories_config = factories_config

    def get_user_content(self) -> str:
        return "Create secrets for a character that are compelling and truly worth being hidden. Follow the provided instructions."

    def create_product_from_base_model(self, response_model: BaseModel):
        return SecretsProduct(response_model.secrets, is_valid=True)

    def get_prompt_file(self) -> Optional[str]:
        return self._path_manager.get_secrets_generation_prompt_path()

    def get_prompt_kwargs(self) -> dict:
        places_descriptions = self._places_descriptions_provider.get_information()

        prompt_data = {"places_descriptions": places_descriptions}

        character = self._factories_config.character_factory.create_character(
            self._config.character_identifier
        )

        prompt_data.update(
            {
                "name": character.name,
                "description": character.description,
                "personality": character.personality,
                "profile": character.profile,
                "likes": character.likes,
                "dislikes": character.dislikes,
                "secrets": character.secrets,
                "speech_patterns": character.speech_patterns,
                "health": character.health,
                "equipment": character.equipment,
            }
        )

        known_facts = self._format_known_facts_algorithm.do_algorithm(
            join_with_newline(
                places_descriptions,
                character.description,
                character.personality,
                character.profile,
                character.likes,
                character.dislikes,
                character.equipment,
            )
        )

        prompt_data.update({"known_facts": known_facts})

        memories = "\n".join(
            self._factories_config.retrieve_memories_algorithm_factory.create_algorithm(
                character.identifier,
                join_with_newline(
                    places_descriptions,
                    known_facts,
                ),
            ).do_algorithm()
        )

        prompt_data.update({"memories": memories})

        return prompt_data
