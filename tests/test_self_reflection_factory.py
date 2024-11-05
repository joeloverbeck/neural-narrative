from pathlib import Path
from typing import cast
from unittest.mock import Mock, patch

import pytest

# Assuming that SelfReflectionFactory is in the module src.self_reflection_factory
from src.base.products.text_product import TextProduct
from src.characters.factories.self_reflection_factory import SelfReflectionFactory
from src.characters.models.self_reflection import SelfReflection, Reflection
from src.filesystem.path_manager import PathManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.abstracts.strategies import ProduceToolResponseStrategy


def test_self_reflection_factory_init_valid_inputs():
    # Arrange
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    character_information_factory = Mock()
    playthrough_name = "test_playthrough"
    character_identifier = "test_character"

    # Act
    factory = SelfReflectionFactory(
        playthrough_name,
        character_identifier,
        cast(
            produce_tool_response_strategy_factory, ProduceToolResponseStrategyFactory
        ),
        character_information_factory,
    )

    # Assert
    assert factory._playthrough_name == playthrough_name
    assert factory._character_identifier == character_identifier
    assert factory._character_information_factory == character_information_factory


def test_self_reflection_factory_init_invalid_playthrough_name():
    # Arrange
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    character_information_factory = Mock()
    playthrough_name = ""
    character_identifier = "test_character"

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        SelfReflectionFactory(
            playthrough_name,
            character_identifier,
            cast(
                produce_tool_response_strategy_factory,
                ProduceToolResponseStrategyFactory,
            ),
            character_information_factory,
        )
    assert "playthrough_name" in str(exc_info.value)


def test_self_reflection_factory_init_invalid_character_identifier():
    # Arrange
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    character_information_factory = Mock()
    playthrough_name = "test_playthrough"
    character_identifier = ""

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        SelfReflectionFactory(
            playthrough_name,
            character_identifier,
            cast(
                produce_tool_response_strategy_factory,
                ProduceToolResponseStrategyFactory,
            ),
            character_information_factory,
        )
    assert "character_identifier" in str(exc_info.value)


def test_get_prompt_file():
    # Arrange
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    character_information_factory = Mock()
    path_manager = Mock(spec=PathManager)
    expected_path = Path("/path/to/prompt")
    path_manager.get_self_reflection_generation_prompt_path.return_value = expected_path

    factory = SelfReflectionFactory(
        "test_playthrough",
        "test_character",
        cast(
            produce_tool_response_strategy_factory, ProduceToolResponseStrategyFactory
        ),
        character_information_factory,
        path_manager=path_manager,
    )

    # Act
    prompt_file = factory.get_prompt_file()

    # Assert
    path_manager.get_self_reflection_generation_prompt_path.assert_called_once()
    assert prompt_file == expected_path


def test_get_user_content():
    # Arrange
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    character_information_factory = Mock()

    factory = SelfReflectionFactory(
        "test_playthrough",
        "test_character",
        cast(
            produce_tool_response_strategy_factory, ProduceToolResponseStrategyFactory
        ),
        character_information_factory,
    )

    # Act
    user_content = factory.get_user_content()

    # Assert
    expected_content = (
        "Write a meaningful and compelling self-reflection from the first-person perspective of the "
        "character regarding their memories. Follow the provided instructions."
    )
    assert user_content == expected_content


def test_create_product_from_base_model():
    # Arrange
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    character_information_factory = Mock()
    factory = SelfReflectionFactory(
        "test_playthrough",
        "test_character",
        cast(
            produce_tool_response_strategy_factory, ProduceToolResponseStrategyFactory
        ),
        character_information_factory,
    )

    response_model = SelfReflection(
        self_reflection=Reflection(
            chain_of_thought="Some chain of thought",
            reflection="First paragraph.\nSecond paragraph.",
        )
    )

    # Act
    with patch(
        "src.characters.factories.self_reflection_factory.logger"
    ) as mock_logger:
        product = factory.create_product_from_base_model(response_model)

        # Assert
        expected_text = "First paragraph.\nSecond paragraph."
        assert isinstance(product, TextProduct)
        assert product.get() == expected_text
        assert product.is_valid() is True

        # Ensure the logger was called with correct chain of thought
        mock_logger.info.assert_called_with(
            "Self-reflection reasoning: %s",
            "Some chain of thought",
        )


def test_get_prompt_kwargs():
    # Arrange
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    character_information_factory = Mock()
    character_information_factory.get_information.return_value = "Character information"

    playthrough_name = "test_playthrough"
    character_identifier = "test_character"

    with patch(
        "src.characters.factories.self_reflection_factory.Character"
    ) as MockCharacter:
        mock_character = MockCharacter.return_value
        mock_character.name = "Test Character"

        factory = SelfReflectionFactory(
            playthrough_name,
            character_identifier,
            cast(
                produce_tool_response_strategy_factory,
                ProduceToolResponseStrategyFactory,
            ),
            character_information_factory,
        )

        # Act
        prompt_kwargs = factory.get_prompt_kwargs()

        # Assert
        MockCharacter.assert_called_once_with(playthrough_name, character_identifier)
        character_information_factory.get_information.assert_called_once()
        assert prompt_kwargs == {
            "name": "Test Character",
            "character_information": "Character information",
        }


def test_generate_product():
    # Arrange
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    character_information_factory = Mock()
    character_information_factory.get_information.return_value = "Character information"

    # Mock the path_manager to return a prompt path
    path_manager = Mock(spec=PathManager)
    prompt_file_path = Path("/path/to/prompt")
    tool_instructions_path = Path("/path/to/tool/instructions")
    path_manager.get_self_reflection_generation_prompt_path.return_value = (
        prompt_file_path
    )
    path_manager.get_tool_instructions_for_instructor_path.return_value = (
        tool_instructions_path
    )

    # Mock read_file to return prompt_template and tool_instructions
    prompt_template = "This is a prompt for {name} with {character_information}."
    tool_instructions = "These are the tool instructions."

    with patch(
        "src.prompting.providers.base_tool_response_provider.read_file",
        side_effect=[prompt_template, tool_instructions],
    ):
        # Mock the strategy and the response model
        produce_tool_response_strategy = Mock(spec=ProduceToolResponseStrategy)
        produce_tool_response_strategy_factory.create_produce_tool_response_strategy.return_value = (
            produce_tool_response_strategy
        )

        produce_tool_response_strategy.produce_tool_response.return_value = (
            SelfReflection(
                self_reflection=Reflection(
                    chain_of_thought="Some chain of thought",
                    reflection="First paragraph.\n\nSecond paragraph.",
                )
            )
        )

        # Mock response_model_class
        response_model_class = SelfReflection

        # Mock Character
        with patch(
            "src.characters.factories.self_reflection_factory.Character"
        ) as MockCharacter:
            mock_character = MockCharacter.return_value
            mock_character.name = "Test Character"

            factory = SelfReflectionFactory(
                "test_playthrough",
                "test_character",
                produce_tool_response_strategy_factory,  # noqa
                character_information_factory,
                path_manager=path_manager,
            )

            # Act
            product = factory.generate_product(response_model_class)

            # Assert
            assert isinstance(product, TextProduct)
            expected_text = "First paragraph.\nSecond paragraph."
            assert product.get() == expected_text
            assert product.is_valid() is True

            # Check that the methods were called correctly
            produce_tool_response_strategy_factory.create_produce_tool_response_strategy.assert_called_once()
            produce_tool_response_strategy.produce_tool_response.assert_called_once()
            character_information_factory.get_information.assert_called_once()


def test_generate_product_invalid_tool_response():
    # Arrange
    produce_tool_response_strategy_factory = Mock(
        spec=ProduceToolResponseStrategyFactory
    )
    character_information_factory = Mock()
    character_information_factory.get_information.return_value = "Character information"

    # Mock the path_manager to return a prompt path
    path_manager = Mock(spec=PathManager)
    prompt_file_path = Path("/path/to/prompt")
    tool_instructions_path = Path("/path/to/tool/instructions")
    path_manager.get_self_reflection_generation_prompt_path.return_value = (
        prompt_file_path
    )
    path_manager.get_tool_instructions_for_instructor_path.return_value = (
        tool_instructions_path
    )

    # Mock read_file to return prompt_template and tool_instructions
    prompt_template = "This is a prompt for {name} with {character_information}."
    tool_instructions = "These are the tool instructions."

    with patch(
        "src.prompting.providers.base_tool_response_provider.read_file",
        side_effect=[prompt_template, tool_instructions],
    ):
        # Mock the strategy
        produce_tool_response_strategy = Mock(spec=ProduceToolResponseStrategy)
        produce_tool_response_strategy_factory.create_produce_tool_response_strategy.return_value = (
            produce_tool_response_strategy
        )

        produce_tool_response_strategy.produce_tool_response.return_value = (
            "Invalid response"
        )

        # Mock response_model_class
        response_model_class = SelfReflection

        # Mock Character
        with patch(
            "src.characters.factories.self_reflection_factory.Character"
        ) as MockCharacter:
            mock_character = MockCharacter.return_value
            mock_character.name = "Test Character"

            factory = SelfReflectionFactory(
                "test_playthrough",
                "test_character",
                produce_tool_response_strategy_factory,  # noqa
                character_information_factory,
                path_manager=path_manager,
            )

            # Act & Assert
            with pytest.raises(NotImplementedError) as exc_info:
                factory.generate_product(response_model_class)

            assert "Case not implemented for when the tool response is of type" in str(
                exc_info.value
            )
