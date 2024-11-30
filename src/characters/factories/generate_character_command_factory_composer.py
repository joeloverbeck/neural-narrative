import logging

from src.base.algorithms.produce_and_update_next_identifier_algorithm import (
    ProduceAndUpdateNextIdentifierAlgorithm,
)
from src.base.enums import IdentifierType
from src.base.factories.store_last_identifier_command_factory import (
    StoreLastIdentifierCommandFactory,
)
from src.characters.factories.character_description_provider_factory import (
    CharacterDescriptionProviderFactory,
)
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.generate_character_command_factory import (
    GenerateCharacterCommandFactory,
)
from src.characters.factories.process_generated_character_data_command_factory import (
    ProcessGeneratedCharacterDataCommandFactory,
)
from src.characters.factories.produce_speech_patterns_algorithm_factory import (
    ProduceSpeechPatternsAlgorithmFactory,
)
from src.characters.factories.speech_patterns_provider_factory import (
    SpeechPatternsProviderFactory,
)
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)
from src.images.factories.openai_generated_image_factory import (
    OpenAIGeneratedImageFactory,
)
from src.maps.composers.places_descriptions_provider_composer import (
    PlacesDescriptionsProviderComposer,
)
from src.movements.factories.place_character_at_place_command_factory import (
    PlaceCharacterAtPlaceCommandFactory,
)
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.factories.character_generation_instructions_formatter_factory import (
    CharacterGenerationInstructionsFormatterFactory,
)
from src.prompting.factories.openai_llm_client_factory import OpenAILlmClientFactory
from src.prompting.llms import Llms
from src.requests.factories.ConcreteUrlContentFactory import ConcreteUrlContentFactory
from src.voices.algorithms.match_voice_data_to_voice_model_algorithm import (
    MatchVoiceDataToVoiceModelAlgorithm,
)
from src.voices.factories.produce_voice_attributes_algorithm_factory import (
    ProduceVoiceAttributesAlgorithmFactory,
)
from src.voices.factories.voice_attributes_provider_factory import (
    VoiceAttributesProviderFactory,
)

logger = logging.getLogger(__name__)


class GenerateCharacterCommandFactoryComposer:

    def __init__(self, playthrough_name: str):
        self._playthrough_name = playthrough_name

    def compose_factory(self) -> GenerateCharacterCommandFactory:
        llms = Llms()

        speech_patterns_produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                llms.for_speech_patterns_generation(),
            ).compose_factory()
        )
        speech_patterns_provider_factory = SpeechPatternsProviderFactory(
            speech_patterns_produce_tool_response_strategy_factory
        )
        match_voice_data_to_voice_model_algorithm = (
            MatchVoiceDataToVoiceModelAlgorithm()
        )

        store_last_identifier_command_factory = StoreLastIdentifierCommandFactory(
            self._playthrough_name
        )

        produce_and_update_next_identifier_algorithm = (
            ProduceAndUpdateNextIdentifierAlgorithm(
                self._playthrough_name,
                IdentifierType.CHARACTERS,
                store_last_identifier_command_factory,
            )
        )

        store_generate_character_command_factory = (
            StoreGeneratedCharacterCommandFactory(
                self._playthrough_name,
                match_voice_data_to_voice_model_algorithm,
                produce_and_update_next_identifier_algorithm,
            )
        )

        character_description_produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                llms.for_character_description(),
            ).compose_factory()
        )

        character_description_provider_factory = CharacterDescriptionProviderFactory(
            character_description_produce_tool_response_strategy_factory
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

        places_description_provider = PlacesDescriptionsProviderComposer(
            self._playthrough_name
        ).compose_provider()
        character_generation_instructions_formatter_factory = (
            CharacterGenerationInstructionsFormatterFactory(
                self._playthrough_name, places_description_provider
            )
        )

        # We need a specific produce_tool_response_strategy_factory given that we pass the BaseModel.
        base_character_data_produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                llms.for_base_character_data_generation(),
            ).compose_factory()
        )

        place_character_at_place_command_factory = PlaceCharacterAtPlaceCommandFactory(
            self._playthrough_name
        )

        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                Llms().for_base_character_data_generation()
            ).compose_factory()
        )

        voice_attributes_provider_factory = VoiceAttributesProviderFactory(
            produce_tool_response_strategy_factory
        )

        produce_voice_attributes_algorithm_factory = (
            ProduceVoiceAttributesAlgorithmFactory(voice_attributes_provider_factory)
        )

        produce_speech_patterns_algorithm_factory = (
            ProduceSpeechPatternsAlgorithmFactory(speech_patterns_provider_factory)
        )

        process_generated_character_data_command_factory = (
            ProcessGeneratedCharacterDataCommandFactory(
                self._playthrough_name,
                store_generate_character_command_factory,
                generate_character_image_command_factory,
                place_character_at_place_command_factory,
            )
        )

        return GenerateCharacterCommandFactory(
            self._playthrough_name,
            character_generation_instructions_formatter_factory,
            base_character_data_produce_tool_response_strategy_factory,
            produce_voice_attributes_algorithm_factory,
            produce_speech_patterns_algorithm_factory,
            process_generated_character_data_command_factory,
        )
