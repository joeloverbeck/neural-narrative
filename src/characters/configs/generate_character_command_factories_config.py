from dataclasses import dataclass

from src.characters.factories.speech_patterns_provider_factory import (
    SpeechPatternsProviderFactory,
)
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.characters.providers.base_character_data_generation_tool_response_provider import (
    BaseCharacterDataGenerationToolResponseProvider,
)
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)
from src.movements.factories.place_character_at_place_command_factory import (
    PlaceCharacterAtPlaceCommandFactory,
)


@dataclass
class GenerateCharacterCommandFactoriesConfig:
    character_generation_tool_response_provider: (
        BaseCharacterDataGenerationToolResponseProvider
    )
    speech_patterns_provider_factory: SpeechPatternsProviderFactory
    store_generate_character_command_factory: StoreGeneratedCharacterCommandFactory
    generate_character_image_command_factory: GenerateCharacterImageCommandFactory
    place_character_at_place_command_factory: PlaceCharacterAtPlaceCommandFactory
