from dataclasses import dataclass

from src.characters.factories.process_generated_character_data_command_factory import (
    ProcessGeneratedCharacterDataCommandFactory,
)
from src.characters.factories.produce_base_character_data_algorithm_factory import (
    ProduceBaseCharacterDataAlgorithmFactory,
)
from src.characters.factories.produce_speech_patterns_algorithm_factory import (
    ProduceSpeechPatternsAlgorithmFactory,
)
from src.voices.factories.produce_voice_attributes_algorithm_factory import (
    ProduceVoiceAttributesAlgorithmFactory,
)


@dataclass
class GenerateCharacterCommandFactoriesConfig:
    produce_base_character_data_algorithm_factory: (
        ProduceBaseCharacterDataAlgorithmFactory
    )
    produce_voice_attributes_algorithm_factory: ProduceVoiceAttributesAlgorithmFactory
    produce_speech_patterns_algorithm_factory: ProduceSpeechPatternsAlgorithmFactory
    process_generated_character_data_command_factory: (
        ProcessGeneratedCharacterDataCommandFactory
    )
