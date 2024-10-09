from src.characters.commands.generate_character_command import GenerateCharacterCommand
from src.characters.factories.character_description_provider_factory import (
    CharacterDescriptionProviderFactory,
)
from src.characters.factories.guidelines_based_user_content_for_character_generation_factory import (
    GuidelinesBasedUserContentForCharacterGenerationFactory,
)
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.characters.providers.character_generation_tool_response_provider import (
    CharacterGenerationToolResponseProvider,
)
from src.config.config_manager import ConfigManager
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)
from src.images.factories.openai_generated_image_factory import (
    OpenAIGeneratedImageFactory,
)
from src.maps.map_manager import MapManager
from src.movements.movement_manager import MovementManager
from src.playthrough_manager import PlaythroughManager
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


class CharacterService:
    @staticmethod
    def add_followers(playthrough_name, character_ids):
        movement_manager = MovementManager(playthrough_name)
        playthrough_manager = PlaythroughManager(playthrough_name)
        for character_id in character_ids:
            movement_manager.add_follower(
                character_id, playthrough_manager.get_current_place_identifier()
            )

    @staticmethod
    def remove_followers(playthrough_name, follower_ids):
        movement_manager = MovementManager(playthrough_name)
        playthrough_manager = PlaythroughManager(playthrough_name)
        for follower_id in follower_ids:
            movement_manager.remove_follower(
                follower_id, playthrough_manager.get_current_place_identifier()
            )

    @staticmethod
    def generate_character(playthrough_name: str, guideline: str):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        if not guideline:
            raise ValueError("guideline can't be empty.")

        map_manager = MapManager(playthrough_name)

        playthrough_manager = PlaythroughManager(playthrough_name)
        places_templates_parameter = map_manager.fill_places_templates_parameter(
            playthrough_manager.get_current_place_identifier()
        )

        llm_client = OpenRouterLlmClientFactory().create_llm_client()

        produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
            llm_client, ConfigManager().get_heavy_llm()
        )

        guided_character_generation_tool_response_provider = (
            CharacterGenerationToolResponseProvider(
                playthrough_name,
                places_templates_parameter,
                produce_tool_response_strategy_factory,
                GuidelinesBasedUserContentForCharacterGenerationFactory(guideline),
            )
        )

        match_voice_data_to_voice_model_algorithm = (
            MatchVoiceDataToVoiceModelAlgorithm()
        )

        store_generate_character_command_factory = (
            StoreGeneratedCharacterCommandFactory(
                playthrough_name, match_voice_data_to_voice_model_algorithm
            )
        )

        generated_image_factory = OpenAIGeneratedImageFactory(
            OpenAILlmClientFactory().create_llm_client()
        )

        url_content_factory = ConcreteUrlContentFactory()

        character_description_provider_factory = CharacterDescriptionProviderFactory(
            produce_tool_response_strategy_factory
        )

        generate_character_image_command_factory = GenerateCharacterImageCommandFactory(
            playthrough_name,
            character_description_provider_factory,
            generated_image_factory,
            url_content_factory,
        )

        # Generate the character
        GenerateCharacterCommand(
            playthrough_name,
            guided_character_generation_tool_response_provider,
            store_generate_character_command_factory,
            generate_character_image_command_factory,
            place_character_at_current_place=True,
        ).execute()
