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
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)
from src.maps.places_templates_parameter import PlacesTemplatesParameter
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class GenerateCharacterCommandFactory:

    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        store_generate_character_command_factory: StoreGeneratedCharacterCommandFactory,
        generate_character_image_command_factory: GenerateCharacterImageCommandFactory,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._store_generate_character_command_factory = (
            store_generate_character_command_factory
        )
        self._generate_character_image_command_factory = (
            generate_character_image_command_factory
        )

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
                ).create_response_provider(places_templates_parameter),
                self._store_generate_character_command_factory,
                self._generate_character_image_command_factory,
                place_character_at_current_place,
            )

        if character_generation_type == CharacterGenerationType.PLAYER_GUIDED:
            return GenerateCharacterCommand(
                self._playthrough_name,
                CharacterGenerationToolResponseProviderFactory(
                    self._playthrough_name,
                    self._produce_tool_response_strategy_factory,
                    PlayerGuidedUserContentForCharacterGenerationFactory(user_content),
                ).create_response_provider(places_templates_parameter),
                self._store_generate_character_command_factory,
                self._generate_character_image_command_factory,
                place_character_at_current_place,
            )

        raise ValueError(f"Not implemented for case '{character_generation_type}'.")
