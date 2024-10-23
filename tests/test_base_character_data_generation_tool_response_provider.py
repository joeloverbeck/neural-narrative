from typing import cast
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from src.characters.models.base_character_data import BaseCharacterData
from src.characters.providers.base_character_data_generation_tool_response_provider import (
    BaseCharacterDataGenerationToolResponseProvider,
)
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
    UserContentForCharacterGenerationFactory,
)
from src.prompting.products.concrete_llm_tool_response_product import (
    ConcreteLlmToolResponseProduct,
)


def test_get_tool_data():
    provider = BaseCharacterDataGenerationToolResponseProvider(
        playthrough_name="test_playthrough",
        places_parameter=MagicMock(),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, MagicMock()
        ),
        user_content_for_character_generation_factory=cast(
            UserContentForCharacterGenerationFactory, MagicMock()
        ),
        character_generation_instructions_formatter_factory=MagicMock(),
    )
    tool_data = provider._get_tool_data()
    expected_schema = BaseCharacterData.model_json_schema()
    assert tool_data == expected_schema


def test_get_formatted_prompt():
    provider = BaseCharacterDataGenerationToolResponseProvider(
        playthrough_name="test_playthrough",
        places_parameter=MagicMock(),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, MagicMock()
        ),
        user_content_for_character_generation_factory=cast(
            UserContentForCharacterGenerationFactory, MagicMock()
        ),
        character_generation_instructions_formatter_factory=MagicMock(),
    )
    templates = {"template_key": "template_value"}
    provider._load_templates = MagicMock(return_value=templates)
    mock_formatter = MagicMock()
    mock_formatter.format.return_value = "formatted_instructions"
    provider._character_generation_instructions_formatter_factory.create_formatter.return_value = (
        mock_formatter
    )

    result = provider.get_formatted_prompt()
    assert result == "formatted_instructions"


def test_get_user_content_valid():
    provider = BaseCharacterDataGenerationToolResponseProvider(
        playthrough_name="test_playthrough",
        places_parameter=MagicMock(),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, MagicMock()
        ),
        user_content_for_character_generation_factory=cast(
            UserContentForCharacterGenerationFactory, MagicMock()
        ),
        character_generation_instructions_formatter_factory=MagicMock(),
    )
    user_content_product = MagicMock()
    user_content_product.is_valid.return_value = True
    user_content_product.get.return_value = "user_content"
    provider._user_content_for_character_generation_factory.create_user_content_for_character_generation.return_value = (
        user_content_product
    )

    result = provider.get_user_content()
    assert result == "user_content"


def test_get_user_content_invalid():
    provider = BaseCharacterDataGenerationToolResponseProvider(
        playthrough_name="test_playthrough",
        places_parameter=MagicMock(),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, MagicMock()
        ),
        user_content_for_character_generation_factory=cast(
            UserContentForCharacterGenerationFactory, MagicMock()
        ),
        character_generation_instructions_formatter_factory=MagicMock(),
    )
    user_content_product = MagicMock()
    user_content_product.is_valid.return_value = False
    user_content_product.get_error.return_value = "error_message"
    provider._user_content_for_character_generation_factory.create_user_content_for_character_generation.return_value = (
        user_content_product
    )

    with pytest.raises(ValueError) as exc_info:
        provider.get_user_content()
    assert (
        "Unable to create user content for character generation: error_message"
        in str(exc_info.value)
    )


def test_create_product_from_base_model():
    provider = BaseCharacterDataGenerationToolResponseProvider(
        playthrough_name="test_playthrough",
        places_parameter=MagicMock(),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, MagicMock()
        ),
        user_content_for_character_generation_factory=cast(
            UserContentForCharacterGenerationFactory, MagicMock()
        ),
        character_generation_instructions_formatter_factory=MagicMock(),
    )
    base_model = MagicMock(spec=BaseModel)
    base_model.name = "Test Name"
    base_model.description = "Test Description"
    base_model.personality = "Test Personality"
    base_model.profile = "Test Profile"
    base_model.likes = "Test Likes"
    base_model.dislikes = "Test Dislikes"
    base_model.secrets = "Test Secrets"
    base_model.health = "Test Health"
    base_model.equipment = "Test Equipment"
    base_model.voice_gender = "male"
    base_model.voice_age = "young"
    base_model.voice_emotion = "happy"
    base_model.voice_tempo = "fast"
    base_model.voice_volume = "loud"
    base_model.voice_texture = "smooth"
    base_model.voice_tone = "warm"
    base_model.voice_style = "formal"
    base_model.voice_personality = "friendly"
    base_model.voice_special_effects = "echo"

    product = provider.create_product_from_base_model(base_model)
    expected_arguments = {
        "name": "Test Name",
        "description": "Test Description",
        "personality": "Test Personality",
        "profile": "Test Profile",
        "likes": "Test Likes",
        "dislikes": "Test Dislikes",
        "secrets": "Test Secrets",
        "health": "Test Health",
        "equipment": "Test Equipment",
        "voice_gender": "male",
        "voice_age": "young",
        "voice_emotion": "happy",
        "voice_tempo": "fast",
        "voice_volume": "loud",
        "voice_texture": "smooth",
        "voice_tone": "warm",
        "voice_style": "formal",
        "voice_personality": "friendly",
        "voice_special_effects": "echo",
    }
    assert isinstance(product, ConcreteLlmToolResponseProduct)
    assert product.get() == expected_arguments
    assert product.is_valid() == True


def test_create_llm_response_success():
    provider = BaseCharacterDataGenerationToolResponseProvider(
        playthrough_name="test_playthrough",
        places_parameter=MagicMock(),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, MagicMock()
        ),
        user_content_for_character_generation_factory=cast(
            UserContentForCharacterGenerationFactory, MagicMock()
        ),
        character_generation_instructions_formatter_factory=MagicMock(),
    )
    # Mock generate_product to return a valid product
    valid_product = MagicMock()
    provider.generate_product = MagicMock(return_value=valid_product)

    result = provider.create_llm_response()
    assert result == valid_product


def test_create_llm_response_exception():
    provider = BaseCharacterDataGenerationToolResponseProvider(
        playthrough_name="test_playthrough",
        places_parameter=MagicMock(),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, MagicMock()
        ),
        user_content_for_character_generation_factory=cast(
            UserContentForCharacterGenerationFactory, MagicMock()
        ),
        character_generation_instructions_formatter_factory=MagicMock(),
    )
    # Mock generate_product to raise exception
    provider.generate_product = MagicMock(side_effect=Exception("Test Exception"))

    with patch("src.base.tools.capture_traceback") as mock_capture_traceback:
        result = provider.create_llm_response()
        assert isinstance(result, ConcreteLlmToolResponseProduct)
        assert not result.is_valid()
        assert (
            "An error occurred while creating the LLM response: Test Exception"
            == result.get_error()
        )


def test_get_location_details_with_location():
    places_parameter = MagicMock()
    places_parameter.get_location_template.return_value = "Test Location"
    provider = BaseCharacterDataGenerationToolResponseProvider(
        playthrough_name="test_playthrough",
        places_parameter=places_parameter,
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, MagicMock()
        ),
        user_content_for_character_generation_factory=cast(
            UserContentForCharacterGenerationFactory, MagicMock()
        ),
        character_generation_instructions_formatter_factory=MagicMock(),
    )
    locations_templates = {"Test Location": {"description": "Location Description"}}
    location_name, location_description = provider._get_location_details(
        locations_templates
    )
    assert location_name == "Location: Test Location:\n"
    assert location_description == "Location Description"


def test_get_location_details_without_location():
    places_parameter = MagicMock()
    places_parameter.get_location_template.return_value = None
    provider = BaseCharacterDataGenerationToolResponseProvider(
        playthrough_name="test_playthrough",
        places_parameter=places_parameter,
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, MagicMock()
        ),
        user_content_for_character_generation_factory=cast(
            UserContentForCharacterGenerationFactory, MagicMock()
        ),
        character_generation_instructions_formatter_factory=MagicMock(),
    )
    locations_templates = {}
    location_name, location_description = provider._get_location_details(
        locations_templates
    )
    assert location_name == ""
    assert location_description == ""


def test_generate_product_integration():
    # This test checks the integration of multiple methods
    filesystem_manager = MagicMock()
    filesystem_manager.read_file.return_value = "tool_instructions"
    filesystem_manager.load_existing_or_new_json_file.return_value = {}
    filesystem_manager.get_file_path_to_playthrough_metadata.return_value = (
        "path/to/metadata"
    )

    produce_tool_response_strategy_factory = MagicMock()
    strategy = MagicMock()
    produce_tool_response_strategy_factory.create_produce_tool_response_strategy.return_value = (
        strategy
    )
    strategy.produce_tool_response.return_value = BaseCharacterData(
        name="Test Name",
        description="Test Description",
        personality="Test Personality",
        profile="Test Profile",
        likes="Test Likes",
        dislikes="Test Dislikes",
        secrets="Test Secrets",
        health="Test Health",
        equipment="Test Equipment",
        voice_gender="MALE",
        voice_age="TEENAGE",
        voice_emotion="HAPPY/JOYFUL",
        voice_tempo="FAST",
        voice_volume="LOUD",
        voice_texture="SMOOTH",
        voice_tone="WARM",
        voice_style="FORMAL",
        voice_personality="YOUTHFUL",
        voice_special_effects="NO SPECIAL EFFECTS",
    )

    user_content_for_character_generation_factory = MagicMock()
    user_content_product = MagicMock()
    user_content_product.is_valid.return_value = True
    user_content_product.get.return_value = "user_content"
    user_content_for_character_generation_factory.create_user_content_for_character_generation.return_value = (
        user_content_product
    )

    character_generation_instructions_formatter_factory = MagicMock()
    formatter = MagicMock()
    formatter.format.return_value = "formatted_instructions"
    character_generation_instructions_formatter_factory.create_formatter.return_value = (
        formatter
    )

    provider = BaseCharacterDataGenerationToolResponseProvider(
        playthrough_name="test_playthrough",
        places_parameter=MagicMock(),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        user_content_for_character_generation_factory=cast(
            UserContentForCharacterGenerationFactory,
            user_content_for_character_generation_factory,
        ),
        character_generation_instructions_formatter_factory=character_generation_instructions_formatter_factory,
        filesystem_manager=filesystem_manager,
    )

    product = provider.generate_product()
    assert isinstance(product, ConcreteLlmToolResponseProduct)
    assert product.is_valid()
    assert product.get()["name"] == "Test Name"


def test_peep_into_system_content():
    # Ensure peep_into_system_content does not alter the system_content
    provider = BaseCharacterDataGenerationToolResponseProvider(
        playthrough_name="test_playthrough",
        places_parameter=MagicMock(),
        produce_tool_response_strategy_factory=cast(
            ProduceToolResponseStrategyFactory, MagicMock()
        ),
        user_content_for_character_generation_factory=cast(
            UserContentForCharacterGenerationFactory, MagicMock()
        ),
        character_generation_instructions_formatter_factory=MagicMock(),
    )
    system_content = "some system content"
    provider.peep_into_system_content(system_content)  # Should not raise any exception
