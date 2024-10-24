from typing import cast
from unittest.mock import MagicMock, patch

from src.base.constants import CONNECTION_GENERATION_PROMPT_FILE
# Import the classes from your code
from src.characters.factories.connection_factory import ConnectionFactory
from src.characters.models.connection import Connection
from src.characters.products.connection_product import ConnectionProduct
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


def test_get_tool_data():
    # Arrange
    character_a_identifier = "char_a"
    character_b_identifier = "char_b"
    character_factory = MagicMock()
    character_information_provider_factory = MagicMock()
    produce_tool_response_strategy_factory = MagicMock()
    filesystem_manager = MagicMock()

    cf = ConnectionFactory(
        character_a_identifier,
        character_b_identifier,
        character_factory,
        character_information_provider_factory,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager,
    )

    # Act
    tool_data = cf._get_tool_data(Connection)

    # Assert
    expected_schema = Connection.model_json_schema()
    assert tool_data == expected_schema


def test_get_user_content():
    # Arrange
    character_a_identifier = "char_a"
    character_b_identifier = "char_b"
    character_factory = MagicMock()
    character_information_provider_factory = MagicMock()
    produce_tool_response_strategy_factory = MagicMock()
    filesystem_manager = MagicMock()

    cf = ConnectionFactory(
        character_a_identifier,
        character_b_identifier,
        character_factory,
        character_information_provider_factory,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager,
    )

    # Act
    user_content = cf.get_user_content()

    # Assert
    expected_content = "Generate a meaningful and compelling connection between the two provided characters. Follow the instructions."
    assert user_content == expected_content


def test_create_product_from_base_model():
    # Arrange
    character_a_identifier = "char_a"
    character_b_identifier = "char_b"
    character_factory = MagicMock()
    character_information_provider_factory = MagicMock()
    produce_tool_response_strategy_factory = MagicMock()
    filesystem_manager = MagicMock()

    cf = ConnectionFactory(
        character_a_identifier,
        character_b_identifier,
        character_factory,
        character_information_provider_factory,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager,
    )

    connection_text = "They are siblings separated at birth."
    base_model = Connection(connection=connection_text)

    # Act
    product = cf.create_product_from_base_model(base_model)

    # Assert
    assert isinstance(product, ConnectionProduct)
    assert product.get() == connection_text
    assert product.is_valid()


def test_get_prompt_file():
    # Arrange
    character_a_identifier = "char_a"
    character_b_identifier = "char_b"
    character_factory = MagicMock()
    character_information_provider_factory = MagicMock()
    produce_tool_response_strategy_factory = MagicMock()
    filesystem_manager = MagicMock()

    cf = ConnectionFactory(
        character_a_identifier,
        character_b_identifier,
        character_factory,
        character_information_provider_factory,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager,
    )

    # Act
    prompt_file = cf.get_prompt_file()

    # Assert
    assert prompt_file == CONNECTION_GENERATION_PROMPT_FILE


def test_get_prompt_kwargs():
    # Arrange
    character_a_identifier = "char_a"
    character_b_identifier = "char_b"

    character_factory = MagicMock()
    character_information_provider_factory = MagicMock()
    produce_tool_response_strategy_factory = MagicMock()
    filesystem_manager = MagicMock()

    # Mock character_factory.create_character(identifier)
    character_a = MagicMock()
    character_a.name = "Alice"
    character_b = MagicMock()
    character_b.name = "Bob"

    def create_character_side_effect(identifier):
        if identifier == "char_a":
            return character_a
        elif identifier == "char_b":
            return character_b
        else:
            raise ValueError("Unknown character identifier")

    character_factory.create_character.side_effect = create_character_side_effect

    # Mock character_information_provider_factory.create_provider(identifier).get_information()
    character_a_info_provider = MagicMock()
    character_a_info_provider.get_information.return_value = "Alice is a brave warrior."
    character_b_info_provider = MagicMock()
    character_b_info_provider.get_information.return_value = "Bob is a cunning thief."

    def create_provider_side_effect(identifier):
        if identifier == "char_a":
            return character_a_info_provider
        elif identifier == "char_b":
            return character_b_info_provider
        else:
            raise ValueError("Unknown character identifier")

    character_information_provider_factory.create_provider.side_effect = (
        create_provider_side_effect
    )

    cf = ConnectionFactory(
        character_a_identifier,
        character_b_identifier,
        character_factory,
        character_information_provider_factory,
        cast(
            ProduceToolResponseStrategyFactory, produce_tool_response_strategy_factory
        ),
        filesystem_manager,
    )

    # Act
    prompt_kwargs = cf.get_prompt_kwargs()

    # Assert
    expected_prompt_kwargs = {
        "character_a_information": "Alice is a brave warrior.",
        "character_b_information": "Bob is a cunning thief.",
        "name_a": "Alice",
        "name_b": "Bob",
    }
    assert prompt_kwargs == expected_prompt_kwargs


def test_generate_product():
    # Arrange
    character_a_identifier = "char_a"
    character_b_identifier = "char_b"

    character_factory = MagicMock()
    character_information_provider_factory = MagicMock()
    produce_tool_response_strategy_factory = MagicMock()
    filesystem_manager = MagicMock()

    # Mock character_factory.create_character(identifier)
    character_a = MagicMock()
    character_a.name = "Alice"
    character_b = MagicMock()
    character_b.name = "Bob"

    def create_character_side_effect(identifier):
        if identifier == "char_a":
            return character_a
        elif identifier == "char_b":
            return character_b
        else:
            raise ValueError("Unknown character identifier")

    character_factory.create_character.side_effect = create_character_side_effect

    # Mock character_information_provider_factory.create_provider(identifier).get_information()
    character_a_info_provider = MagicMock()
    character_a_info_provider.get_information.return_value = "Alice is a brave warrior."
    character_b_info_provider = MagicMock()
    character_b_info_provider.get_information.return_value = "Bob is a cunning thief."

    def create_provider_side_effect(identifier):
        if identifier == "char_a":
            return character_a_info_provider
        elif identifier == "char_b":
            return character_b_info_provider
        else:
            raise ValueError("Unknown character identifier")

    character_information_provider_factory.create_provider.side_effect = (
        create_provider_side_effect
    )

    # Mock filesystem_manager.read_file
    prompt_template = "This is a prompt for {name_a} and {name_b}."

    def read_file_side_effect(file_path):
        if file_path == CONNECTION_GENERATION_PROMPT_FILE:
            return prompt_template
        elif file_path == "path/to/tool_instructions":
            return "These are tool instructions."
        else:
            return ""

    filesystem_manager.read_file.side_effect = read_file_side_effect

    # Mock the tool instructions constant
    with patch(
        "src.base.constants.TOOL_INSTRUCTIONS_FOR_INSTRUCTOR_FILE",
        "path/to/tool_instructions",
    ):
        # Mock produce_tool_response_strategy_factory
        strategy = MagicMock()
        strategy.produce_tool_response.return_value = Connection(
            connection="They are old friends."
        )
        produce_tool_response_strategy_factory.create_produce_tool_response_strategy.return_value = (
            strategy
        )

        cf = ConnectionFactory(
            character_a_identifier,
            character_b_identifier,
            character_factory,
            character_information_provider_factory,
            cast(
                ProduceToolResponseStrategyFactory,
                produce_tool_response_strategy_factory,
            ),
            filesystem_manager,
        )

        # Act
        product = cf.generate_product(Connection)

        # Assert
        assert isinstance(product, ConnectionProduct)
        assert product.get() == "They are old friends."
        assert product.is_valid()

        # Ensure the strategy was called with the correct system_content and user_content
        (
            "This is a prompt for Alice and Bob.\n\nThese are tool instructions. "
            + str(Connection.model_json_schema())
        )
        strategy.produce_tool_response.assert_called_once()
