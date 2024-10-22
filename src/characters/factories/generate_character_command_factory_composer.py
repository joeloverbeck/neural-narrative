import logging

from src.characters.factories.character_description_provider_factory import (
    CharacterDescriptionProviderFactory,
)
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.generate_character_command_factory import (
    GenerateCharacterCommandFactory,
)
from src.characters.factories.speech_patterns_provider_factory import (
    SpeechPatternsProviderFactory,
)
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.config.config_manager import ConfigManager
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)
from src.images.factories.openai_generated_image_factory import (
    OpenAIGeneratedImageFactory,
)
from src.maps.composers.places_descriptions_provider_composer import (
    PlacesDescriptionsProviderComposer,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.movements.movement_manager import MovementManager
from src.prompting.factories.character_generation_instructions_formatter_factory import (
    CharacterGenerationInstructionsFormatterFactory,
)
from src.prompting.factories.openai_llm_client_factory import OpenAILlmClientFactory
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.requests.factories.ConcreteUrlContentFactory import ConcreteUrlContentFactory
from src.voices.algorithms.match_voice_data_to_voice_model_algorithm import (
    MatchVoiceDataToVoiceModelAlgorithm,
)

logger = logging.getLogger(__name__)


class GenerateCharacterCommandFactoryComposer:

    def __init__(self, playthrough_name: str):
        self._playthrough_name = playthrough_name

    def compose_factory(self) -> GenerateCharacterCommandFactory:
        produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
            OpenRouterLlmClientFactory().create_llm_client(),
            ConfigManager().get_heavy_llm(),
        )
        speech_patterns_provider_factory = SpeechPatternsProviderFactory(
            produce_tool_response_strategy_factory
        )
        match_voice_data_to_voice_model_algorithm = (
            MatchVoiceDataToVoiceModelAlgorithm()
        )
        store_generate_character_command_factory = (
            StoreGeneratedCharacterCommandFactory(
                self._playthrough_name, match_voice_data_to_voice_model_algorithm
            )
        )
        character_description_provider_factory = CharacterDescriptionProviderFactory(
            produce_tool_response_strategy_factory
        )
        generated_image_factory = OpenAIGeneratedImageFactory(
            OpenAILlmClientFactory().create_llm_client()
        )
        url_content_factory = ConcreteUrlContentFactory()
        character_factory = CharacterFactory(self._playthrough_name)
        generate_character_image_command_factory = GenerateCharacterImageCommandFactory(
            self._playthrough_name,
            character_factory,
            character_description_provider_factory,
            generated_image_factory,
            url_content_factory,
        )
        place_manager_factory = PlaceManagerFactory(self._playthrough_name)
        movement_manager = MovementManager(
            self._playthrough_name, place_manager_factory
        )
        places_description_provider = PlacesDescriptionsProviderComposer(
            self._playthrough_name
        ).compose_provider()
        character_generation_instructions_formatter_factory = (
            CharacterGenerationInstructionsFormatterFactory(
                self._playthrough_name, places_description_provider
            )
        )
        return GenerateCharacterCommandFactory(
            self._playthrough_name,
            character_generation_instructions_formatter_factory,
            produce_tool_response_strategy_factory,
            speech_patterns_provider_factory,
            store_generate_character_command_factory,
            generate_character_image_command_factory,
            movement_manager,
        )
