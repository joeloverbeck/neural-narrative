from typing import Optional
from unittest.mock import Mock
import pytest
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class TestToolResponseProvider(BaseToolResponseProvider):

    def get_tool_file(self) -> str:
        return "tool_file.json"

    def get_user_content(self) -> str:
        return "user content"

    def create_product(self, arguments: dict):
        return "product created with arguments: {}".format(arguments)

    def get_prompt_file(self) -> Optional[str]:
        return "prompt_file.txt"

    def get_prompt_kwargs(self) -> dict:
        return {"key": "value"}

    def get_formatted_prompt(self) -> Optional[str]:
        return None

    def _read_tool_instructions(self) -> str:
        return "Tool Instructions with {tool_name} and {tool_description}"


def test_base_tool_response_provider_init_with_none_filesystem_manager():
    mock_strategy_factory = Mock(spec=ProduceToolResponseStrategyFactory)
    provider = BaseToolResponseProvider(mock_strategy_factory, None)
    assert isinstance(provider._filesystem_manager, FilesystemManager)


def test_read_prompt_file_reads_file_correctly():
    mock_strategy_factory = Mock(spec=ProduceToolResponseStrategyFactory)
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    mock_filesystem_manager.read_file.return_value = "Prompt Content"
    provider = TestToolResponseProvider(mock_strategy_factory, mock_filesystem_manager)
    prompt_file = "prompt_file.txt"
    result = provider._read_prompt_file(prompt_file)
    assert result == "Prompt Content"
    mock_filesystem_manager.read_file.assert_called_once_with(prompt_file)


def test_read_tool_file_reads_json_correctly():
    mock_strategy_factory = Mock(spec=ProduceToolResponseStrategyFactory)
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    mock_tool_data = {"function": {"name": "test_tool", "description": "A test tool"}}
    mock_filesystem_manager.read_json_file.return_value = mock_tool_data
    provider = TestToolResponseProvider(mock_strategy_factory, mock_filesystem_manager)
    tool_file = "tool_file.json"
    result = provider._read_tool_file(tool_file)
    assert result == mock_tool_data
    mock_filesystem_manager.read_json_file.assert_called_once_with(tool_file)


def test_generate_tool_prompt():
    tool_data = {
        "function": {"name": "test_tool", "description": "A test tool", "other": "data"}
    }
    tool_instructions = (
        "Use the {tool_name} which is {tool_description}. Details: {tool}"
    )
    expected_output = 'Use the test_tool which is A test tool. Details: {"name": "test_tool", "description": "A test tool", "other": "data"}'
    result = BaseToolResponseProvider._generate_tool_prompt(
        tool_data, tool_instructions
    )
    assert result == expected_output


def test_format_prompt():
    prompt_template = "Hello, {name}!"
    kwargs = {"name": "World"}
    expected_output = "Hello, World!"
    result = BaseToolResponseProvider._format_prompt(prompt_template, **kwargs)
    assert result == expected_output


def test_format_prompt_with_missing_key():
    prompt_template = "Hello, {name}! Your age is {age}."
    kwargs = {"name": "Alice"}
    with pytest.raises(KeyError) as exc_info:
        BaseToolResponseProvider._format_prompt(prompt_template, **kwargs)
    assert "'age'" in str(exc_info)


def test_generate_system_content():
    prompt = "This is the prompt."
    tool_prompt = "This is the tool prompt."
    expected_output = "This is the prompt.\n\nThis is the tool prompt."
    result = BaseToolResponseProvider._generate_system_content(prompt, tool_prompt)
    assert result == expected_output


def test_produce_tool_response_calls_strategy():
    mock_strategy = Mock()
    mock_strategy.produce_tool_response.return_value = {"arguments": {"arg1": "value1"}}
    mock_strategy_factory = Mock()
    (mock_strategy_factory.create_produce_tool_response_strategy.return_value) = (
        mock_strategy
    )
    provider = TestToolResponseProvider(mock_strategy_factory)
    system_content = "System content"
    user_content = "User content"
    result = provider._produce_tool_response(system_content, user_content)
    assert result == {"arguments": {"arg1": "value1"}}
    mock_strategy.produce_tool_response.assert_called_once_with(
        system_content, user_content
    )


def test_extract_arguments():
    tool_response = {"arguments": {"arg1": "value1"}}
    expected_arguments = {"arg1": "value1"}
    result = BaseToolResponseProvider._extract_arguments(tool_response)
    assert result == expected_arguments


def test_extract_arguments_no_arguments_key():
    tool_response = {"other_key": "other_value"}
    expected_arguments = {}
    result = BaseToolResponseProvider._extract_arguments(tool_response)
    assert result == expected_arguments


def test_generate_product():
    mock_strategy = Mock()
    mock_strategy.produce_tool_response.return_value = {"arguments": {"arg1": "value1"}}
    mock_strategy_factory = Mock()
    (mock_strategy_factory.create_produce_tool_response_strategy.return_value) = (
        mock_strategy
    )
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    mock_filesystem_manager.read_file.side_effect = ["Prompt template with {key}"]
    mock_tool_data = {
        "function": {"name": "test_tool", "description": "A test tool", "other": "data"}
    }
    mock_filesystem_manager.read_json_file.return_value = mock_tool_data
    provider = TestToolResponseProvider(mock_strategy_factory, mock_filesystem_manager)
    product = provider.generate_product()
    expected_product = "product created with arguments: {}".format({"arg1": "value1"})
    assert product == expected_product
    mock_filesystem_manager.read_file.assert_called_once_with("prompt_file.txt")
    mock_filesystem_manager.read_json_file.assert_called_once_with("tool_file.json")
    mock_strategy.produce_tool_response.assert_called_once()
    system_content_arg = mock_strategy.produce_tool_response.call_args[0][0]
    user_content_arg = mock_strategy.produce_tool_response.call_args[0][1]
    expected_system_content = """Prompt template with value

Tool Instructions with test_tool and A test tool"""
    assert system_content_arg == expected_system_content
    assert user_content_arg == "user content"


def test_generate_product_with_formatted_prompt():
    mock_strategy = Mock()
    mock_strategy.produce_tool_response.return_value = {"arguments": {"arg1": "value1"}}
    mock_strategy_factory = Mock()
    (mock_strategy_factory.create_produce_tool_response_strategy.return_value) = (
        mock_strategy
    )
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    mock_tool_data = {
        "function": {"name": "test_tool", "description": "A test tool", "other": "data"}
    }
    mock_filesystem_manager.read_json_file.return_value = mock_tool_data

    class TestProvider(TestToolResponseProvider):

        def get_formatted_prompt(self) -> Optional[str]:
            return "Pre-formatted prompt"

    provider = TestProvider(mock_strategy_factory, mock_filesystem_manager)
    product = provider.generate_product()
    expected_product = "product created with arguments: {}".format({"arg1": "value1"})
    assert product == expected_product
    mock_filesystem_manager.read_file.assert_not_called()
    mock_filesystem_manager.read_json_file.assert_called_once_with("tool_file.json")
    mock_strategy.produce_tool_response.assert_called_once()
    system_content_arg = mock_strategy.produce_tool_response.call_args[0][0]
    expected_system_content = """Pre-formatted prompt

Tool Instructions with test_tool and A test tool"""
    assert system_content_arg == expected_system_content


def test_produce_tool_response_strategy_exception():
    mock_strategy = Mock()
    mock_strategy.produce_tool_response.side_effect = Exception("Strategy error")
    mock_strategy_factory = Mock()
    (mock_strategy_factory.create_produce_tool_response_strategy.return_value) = (
        mock_strategy
    )
    provider = TestToolResponseProvider(mock_strategy_factory)
    system_content = "System content"
    user_content = "User content"
    with pytest.raises(Exception) as exc_info:
        provider._produce_tool_response(system_content, user_content)
    assert "Strategy error" in str(exc_info)


def test_generate_tool_prompt_with_missing_keys():
    tool_data = {"function": {"name": "test_tool"}}
    tool_instructions = "Use the {tool_name} which is {tool_description}."
    with pytest.raises(KeyError) as exc_info:
        BaseToolResponseProvider._generate_tool_prompt(tool_data, tool_instructions)
    assert "'description'" in str(exc_info)


def test_read_prompt_file_file_not_found():
    mock_strategy_factory = Mock(spec=ProduceToolResponseStrategyFactory)
    mock_filesystem_manager = Mock(spec=FilesystemManager)
    mock_filesystem_manager.read_file.side_effect = FileNotFoundError("File not found")
    provider = TestToolResponseProvider(mock_strategy_factory, mock_filesystem_manager)
    prompt_file = "nonexistent_prompt_file.txt"
    with pytest.raises(FileNotFoundError) as exc_info:
        provider._read_prompt_file(prompt_file)
    assert "File not found" in str(exc_info)
