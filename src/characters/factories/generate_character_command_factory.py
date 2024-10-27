import logging

from src.characters.commands.generate_character_command import GenerateCharacterCommand
from src.characters.configs.generate_character_command_config import (
    GenerateCharacterCommandConfig,
)
from src.characters.configs.generate_character_command_factories_config import (
    GenerateCharacterCommandFactoriesConfig,
)
from src.characters.enums import CharacterGenerationType
from src.characters.factories.automatic_user_content_for_character_generation_factory import (
    AutomaticUserContentForCharacterGenerationFactory,
)
from src.characters.factories.base_character_data_generation_tool_response_provider_factory import (
    BaseCharacterDataGenerationToolResponseProviderFactory,
)
from src.characters.factories.player_guided_user_content_for_character_generation_factory import (
    PlayerGuidedUserContentForCharacterGenerationFactory,
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
from src.movements.factories.place_character_at_place_command_factory import (
    PlaceCharacterAtPlaceCommandFactory,
)
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.factories.character_generation_instructions_formatter_factory import (
    CharacterGenerationInstructionsFormatterFactory,
)

logger = logging.getLogger(__name__)


class GenerateCharacterCommandFactory:

    def __init__(
        self,
        playthrough_name: str,
        character_generation_instructions_formatter_factory: CharacterGenerationInstructionsFormatterFactory,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        speech_patterns_provider_factory: SpeechPatternsProviderFactory,
        store_generate_character_command_factory: StoreGeneratedCharacterCommandFactory,
        generate_character_image_command_factory: GenerateCharacterImageCommandFactory,
        place_character_at_place_command_factory: PlaceCharacterAtPlaceCommandFactory,
    ):
        self._playthrough_name = playthrough_name
        self._character_generation_instructions_formatter_factory = (
            character_generation_instructions_formatter_factory
        )
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._speech_patterns_provider_factory = speech_patterns_provider_factory
        self._store_generate_character_command_factory = (
            store_generate_character_command_factory
        )
        self._generate_character_image_command_factory = (
            generate_character_image_command_factory
        )
        self._place_character_at_place_command_factory = (
            place_character_at_place_command_factory
        )

    def create_generate_character_command(
        self,
        place_character_at_current_place: bool,
        user_content: str,
    ):
        character_generation_type = (
            CharacterGenerationType.PLAYER_GUIDED
            if user_content
            else CharacterGenerationType.AUTOMATIC
        )
        if character_generation_type == CharacterGenerationType.AUTOMATIC:
            return GenerateCharacterCommand(
                GenerateCharacterCommandConfig(
                    self._playthrough_name, place_character_at_current_place
                ),
                GenerateCharacterCommandFactoriesConfig(
                    BaseCharacterDataGenerationToolResponseProviderFactory(
                        self._playthrough_name,
                        self._produce_tool_response_strategy_factory,
                        AutomaticUserContentForCharacterGenerationFactory(),
                        self._character_generation_instructions_formatter_factory,
                    ).create_response_provider(),
                    self._speech_patterns_provider_factory,
                    self._store_generate_character_command_factory,
                    self._generate_character_image_command_factory,
                    self._place_character_at_place_command_factory,
                ),
            )
        if character_generation_type == CharacterGenerationType.PLAYER_GUIDED:
            return GenerateCharacterCommand(
                GenerateCharacterCommandConfig(
                    self._playthrough_name, place_character_at_current_place
                ),
                GenerateCharacterCommandFactoriesConfig(
                    BaseCharacterDataGenerationToolResponseProviderFactory(
                        self._playthrough_name,
                        self._produce_tool_response_strategy_factory,
                        PlayerGuidedUserContentForCharacterGenerationFactory(
                            user_content
                        ),
                        self._character_generation_instructions_formatter_factory,
                    ).create_response_provider(),
                    self._speech_patterns_provider_factory,
                    self._store_generate_character_command_factory,
                    self._generate_character_image_command_factory,
                    self._place_character_at_place_command_factory,
                ),
            )
        raise ValueError(f"Not implemented for case '{character_generation_type}'.")
