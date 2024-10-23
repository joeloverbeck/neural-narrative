import logging

from src.characters.commands.generate_character_command import GenerateCharacterCommand
from src.characters.enums import CharacterGenerationType
from src.characters.factories.automatic_user_content_for_character_generation_factory import (
    AutomaticUserContentForCharacterGenerationFactory,
)
from src.characters.factories.character_generation_tool_response_provider_factory import (
    CharacterGenerationToolResponseProviderFactory,
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
from src.maps.places_templates_parameter import PlacesTemplatesParameter
from src.movements.movement_manager import MovementManager
from src.prompting.factories.character_generation_instructions_formatter_factory import (
    CharacterGenerationInstructionsFormatterFactory,
)
from src.prompting.factories.unparsed_string_produce_tool_response_strategy_factory import (
    UnparsedStringProduceToolResponseStrategyFactory,
)

logger = logging.getLogger(__name__)


class GenerateCharacterCommandFactory:

    def __init__(
        self,
        playthrough_name: str,
        character_generation_instructions_formatter_factory: CharacterGenerationInstructionsFormatterFactory,
        produce_tool_response_strategy_factory: UnparsedStringProduceToolResponseStrategyFactory,
        speech_patterns_provider_factory: SpeechPatternsProviderFactory,
        store_generate_character_command_factory: StoreGeneratedCharacterCommandFactory,
        generate_character_image_command_factory: GenerateCharacterImageCommandFactory,
        movement_manager: MovementManager,
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
        self._movement_manager = movement_manager

    def create_generate_character_command(
        self,
        places_templates_parameter: PlacesTemplatesParameter,
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
                self._playthrough_name,
                CharacterGenerationToolResponseProviderFactory(
                    self._playthrough_name,
                    self._produce_tool_response_strategy_factory,
                    AutomaticUserContentForCharacterGenerationFactory(),
                    self._character_generation_instructions_formatter_factory,
                ).create_response_provider(places_templates_parameter),
                self._speech_patterns_provider_factory,
                self._store_generate_character_command_factory,
                self._generate_character_image_command_factory,
                place_character_at_current_place,
                self._movement_manager,
            )
        if character_generation_type == CharacterGenerationType.PLAYER_GUIDED:
            return GenerateCharacterCommand(
                self._playthrough_name,
                CharacterGenerationToolResponseProviderFactory(
                    self._playthrough_name,
                    self._produce_tool_response_strategy_factory,
                    PlayerGuidedUserContentForCharacterGenerationFactory(user_content),
                    self._character_generation_instructions_formatter_factory,
                ).create_response_provider(places_templates_parameter),
                self._speech_patterns_provider_factory,
                self._store_generate_character_command_factory,
                self._generate_character_image_command_factory,
                place_character_at_current_place,
                self._movement_manager,
            )
        raise ValueError(f"Not implemented for case '{character_generation_type}'.")
