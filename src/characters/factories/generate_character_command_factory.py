import logging

from src.characters.commands.generate_character_command import GenerateCharacterCommand
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
from src.characters.factories.process_generated_character_data_command_factory import (
    ProcessGeneratedCharacterDataCommandFactory,
)
from src.characters.factories.produce_base_character_data_algorithm_factory import (
    ProduceBaseCharacterDataAlgorithmFactory,
)
from src.characters.factories.produce_speech_patterns_algorithm_factory import (
    ProduceSpeechPatternsAlgorithmFactory,
)
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.factories.character_generation_instructions_formatter_factory import (
    CharacterGenerationInstructionsFormatterFactory,
)
from src.voices.factories.produce_voice_attributes_algorithm_factory import (
    ProduceVoiceAttributesAlgorithmFactory,
)

logger = logging.getLogger(__name__)


class GenerateCharacterCommandFactory:

    def __init__(
        self,
        playthrough_name: str,
        character_generation_instructions_formatter_factory: CharacterGenerationInstructionsFormatterFactory,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        produce_voice_attributes_algorithm_factory: ProduceVoiceAttributesAlgorithmFactory,
        produce_speech_patterns_algorithm_factory: ProduceSpeechPatternsAlgorithmFactory,
        process_generated_character_data_command_factory: ProcessGeneratedCharacterDataCommandFactory,
    ):
        self._playthrough_name = playthrough_name
        self._character_generation_instructions_formatter_factory = (
            character_generation_instructions_formatter_factory
        )
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._produce_voice_attributes_algorithm_factory = (
            produce_voice_attributes_algorithm_factory
        )
        self._produce_speech_patterns_algorithm_factory = (
            produce_speech_patterns_algorithm_factory
        )
        self._process_generated_character_data_command_factory = (
            process_generated_character_data_command_factory
        )

    def create_generate_character_command(
        self,
        is_player: bool,
        user_content: str,
    ):
        character_generation_type = (
            CharacterGenerationType.PLAYER_GUIDED
            if user_content
            else CharacterGenerationType.AUTOMATIC
        )

        if character_generation_type == CharacterGenerationType.AUTOMATIC:
            base_character_data_generation_tool_response_provider_factory = (
                BaseCharacterDataGenerationToolResponseProviderFactory(
                    self._playthrough_name,
                    self._produce_tool_response_strategy_factory,
                    AutomaticUserContentForCharacterGenerationFactory(),
                    self._character_generation_instructions_formatter_factory,
                )
            )

            produce_base_character_data_algorithm_factory = (
                ProduceBaseCharacterDataAlgorithmFactory(
                    base_character_data_generation_tool_response_provider_factory
                )
            )

            return GenerateCharacterCommand(
                is_player,
                GenerateCharacterCommandFactoriesConfig(
                    produce_base_character_data_algorithm_factory,
                    self._produce_voice_attributes_algorithm_factory,
                    self._produce_speech_patterns_algorithm_factory,
                    self._process_generated_character_data_command_factory,
                ),
            )

        if character_generation_type == CharacterGenerationType.PLAYER_GUIDED:
            base_character_data_generation_tool_response_provider_factory = (
                BaseCharacterDataGenerationToolResponseProviderFactory(
                    self._playthrough_name,
                    self._produce_tool_response_strategy_factory,
                    PlayerGuidedUserContentForCharacterGenerationFactory(user_content),
                    self._character_generation_instructions_formatter_factory,
                )
            )

            produce_base_character_data_algorithm_factory = (
                ProduceBaseCharacterDataAlgorithmFactory(
                    base_character_data_generation_tool_response_provider_factory
                )
            )

            return GenerateCharacterCommand(
                is_player,
                GenerateCharacterCommandFactoriesConfig(
                    produce_base_character_data_algorithm_factory,
                    self._produce_voice_attributes_algorithm_factory,
                    self._produce_speech_patterns_algorithm_factory,
                    self._process_generated_character_data_command_factory,
                ),
            )

        raise ValueError(f"Not implemented for case '{character_generation_type}'.")
