from unittest.mock import Mock, patch

import pytest

from src.exceptions import VoiceLineGenerationError
from src.voices.algorithms.direct_voice_line_generation_algorithm import (
    DirectVoiceLineGenerationAlgorithm,
)


# Test 1: Initialization with empty text should raise ValueError
def test_init_with_empty_text_raises_value_error():
    with pytest.raises(ValueError, match="text can't be empty."):
        DirectVoiceLineGenerationAlgorithm(
            text="",
            voice_part_provider_factory=Mock(),
            voice_line_file_name_provider_factory=Mock(),
        )


# Test 2: When xtts_endpoint is None, the method should return None
def test_direct_voice_line_generation_no_xtts_endpoint():
    text = "Sample text"
    voice_part_provider_factory = Mock()
    voice_line_file_name_provider_factory = Mock()
    requests_manager = Mock()
    requests_manager.get_xtts_endpoint.return_value = None
    filesystem_manager = Mock()

    algorithm = DirectVoiceLineGenerationAlgorithm(
        text=text,
        voice_part_provider_factory=voice_part_provider_factory,
        voice_line_file_name_provider_factory=voice_line_file_name_provider_factory,
        requests_manager=requests_manager,
        filesystem_manager=filesystem_manager,
    )

    result = algorithm.direct_voice_line_generation()

    assert result is None


# Test 3: The algorithm should process each part of the text
@patch("time.strftime", return_value="20220101010101")
def test_direct_voice_line_generation_processes_each_part(mock_strftime):
    text = "This is *emphasized* text."

    # Mocking dependencies
    voice_part_provider_factory = Mock()
    voice_part_provider = Mock()
    voice_part_provider_factory.create_provider.return_value = voice_part_provider

    voice_line_file_name_provider_factory = Mock()
    voice_line_file_name_provider = Mock()
    voice_line_file_name_provider.provide_file_name.return_value = "output_file.mp3"
    voice_line_file_name_provider_factory.create_factory.return_value = (
        voice_line_file_name_provider
    )

    requests_manager = Mock()
    requests_manager.get_xtts_endpoint.return_value = "http://xtts_endpoint"

    filesystem_manager = Mock()
    filesystem_manager.get_temporary_folder_to_store_voice_parts.return_value = (
        "/temp_dir"
    )

    # Define a side effect for create_voice_part to append to temp_file_paths
    def create_voice_part_side_effect():
        # Retrieve the last call's config to access temp_file_paths
        config = voice_part_provider_factory.create_provider.call_args_list[-1][0][0]
        # Simulate adding a file path to temp_file_paths
        file_path = f"{config.temp_dir}/part{config.index}.mp3"
        config.temp_file_paths.append(file_path)

    voice_part_provider.create_voice_part.side_effect = create_voice_part_side_effect

    # Instantiate the algorithm
    algorithm = DirectVoiceLineGenerationAlgorithm(
        text=text,
        voice_part_provider_factory=voice_part_provider_factory,
        voice_line_file_name_provider_factory=voice_line_file_name_provider_factory,
        requests_manager=requests_manager,
        filesystem_manager=filesystem_manager,
    )

    # Run the method under test
    result = algorithm.direct_voice_line_generation()

    # Expected parts after splitting the text
    expected_parts = ["This is ", "*emphasized*", " text."]

    # Assertions
    assert voice_part_provider_factory.create_provider.call_count == len(expected_parts)
    assert voice_part_provider.create_voice_part.call_count == len(expected_parts)
    assert result == "output_file.mp3"

    # Verify that each part was processed correctly
    calls = voice_part_provider_factory.create_provider.call_args_list
    for index, call in enumerate(calls):
        args, _ = call
        config = args[0]
        assert config.part == expected_parts[index]
        assert config.xtts_endpoint == "http://xtts_endpoint"
        assert config.timestamp == "20220101010101"
        assert config.index == index
        assert config.temp_dir == "/temp_dir"

    # Additionally, verify that temp_file_paths contains the expected file paths
    expected_temp_file_paths = [
        "/temp_dir/part0.mp3",
        "/temp_dir/part1.mp3",
        "/temp_dir/part2.mp3",
    ]
    assert config.temp_file_paths == expected_temp_file_paths

    # Verify that provide_file_name was called with the correct arguments
    voice_line_file_name_provider_factory.create_factory.assert_called_once_with(
        "/temp_dir", expected_temp_file_paths
    )
    voice_line_file_name_provider.provide_file_name.assert_called_once()


# Test 4: If no voice lines are generated, the method should return None
@patch("time.strftime", return_value="20220101010101")
def test_direct_voice_line_generation_no_voice_lines_generated(mock_strftime):
    text = "Sample text with no voice lines generated."

    # Mocking dependencies
    voice_part_provider_factory = Mock()
    voice_part_provider = Mock()
    voice_part_provider_factory.create_provider.return_value = voice_part_provider

    # Mock create_voice_part to not modify temp_file_paths
    def create_voice_part_noop():
        pass  # Does not modify temp_file_paths

    voice_part_provider.create_voice_part.side_effect = create_voice_part_noop

    voice_line_file_name_provider_factory = Mock()
    voice_line_file_name_provider_factory.create_factory.return_value = Mock()

    requests_manager = Mock()
    requests_manager.get_xtts_endpoint.return_value = "http://xtts_endpoint"

    filesystem_manager = Mock()
    filesystem_manager.get_temporary_folder_to_store_voice_parts.return_value = (
        "/temp_dir"
    )

    # Instantiate the algorithm
    algorithm = DirectVoiceLineGenerationAlgorithm(
        text=text,
        voice_part_provider_factory=voice_part_provider_factory,
        voice_line_file_name_provider_factory=voice_line_file_name_provider_factory,
        requests_manager=requests_manager,
        filesystem_manager=filesystem_manager,
    )

    # Run the method under test
    result = algorithm.direct_voice_line_generation()

    # Assertions
    assert result is None


# Test 5: The algorithm should handle exceptions in create_voice_part and continue processing
@patch("time.strftime", return_value="20220101010101")
def test_direct_voice_line_generation_handles_exceptions(mock_strftime):
    text = "Part one. *Part two with error*. Part three."

    # Mocking dependencies
    voice_part_provider_factory = Mock()
    voice_part_provider = Mock()
    voice_part_provider_factory.create_provider.return_value = voice_part_provider

    temp_file_paths = []

    # Define side effects for create_voice_part
    def create_voice_part_side_effect():
        call_index = voice_part_provider.create_voice_part.call_count - 1
        config = voice_part_provider_factory.create_provider.call_args_list[call_index][
            0
        ][0]
        if call_index == 1:
            raise VoiceLineGenerationError("Failed to generate voice line.")
        else:
            temp_file_path = f"/temp_dir/part{config.index}.mp3"
            config.temp_file_paths.append(temp_file_path)

    voice_part_provider.create_voice_part.side_effect = create_voice_part_side_effect

    voice_line_file_name_provider_factory = Mock()
    voice_line_file_name_provider = Mock()
    voice_line_file_name_provider.provide_file_name.return_value = "output_file.mp3"
    voice_line_file_name_provider_factory.create_factory.return_value = (
        voice_line_file_name_provider
    )

    requests_manager = Mock()
    requests_manager.get_xtts_endpoint.return_value = "http://xtts_endpoint"

    filesystem_manager = Mock()
    filesystem_manager.get_temporary_folder_to_store_voice_parts.return_value = (
        "/temp_dir"
    )

    # Instantiate the algorithm
    algorithm = DirectVoiceLineGenerationAlgorithm(
        text=text,
        voice_part_provider_factory=voice_part_provider_factory,
        voice_line_file_name_provider_factory=voice_line_file_name_provider_factory,
        requests_manager=requests_manager,
        filesystem_manager=filesystem_manager,
    )

    # Run the method under test
    result = algorithm.direct_voice_line_generation()

    # Expected temp_file_paths after processing
    expected_temp_file_paths = ["/temp_dir/part0.mp3", "/temp_dir/part2.mp3"]

    # Assertions
    assert result == "output_file.mp3"

    # Verify temp_file_paths
    config_calls = voice_part_provider_factory.create_provider.call_args_list
    final_temp_file_paths = config_calls[0][0][0].temp_file_paths
    assert final_temp_file_paths == expected_temp_file_paths

    # Ensure that the exception was handled and processing continued
    assert voice_part_provider.create_voice_part.call_count == 3


# Test 6: If temp_file_paths is not empty, provide_file_name should be called
@patch("time.strftime", return_value="20220101010101")
def test_direct_voice_line_generation_calls_provide_file_name(mock_strftime):
    text = "Generate voice lines for this text."

    # Mocking dependencies
    voice_part_provider_factory = Mock()
    voice_part_provider = Mock()
    voice_part_provider_factory.create_provider.return_value = voice_part_provider

    # Simulate successful voice part creation
    def create_voice_part_success():
        config = voice_part_provider_factory.create_provider.call_args_list[-1][0][0]
        temp_file_path = f"/temp_dir/part{config.index}.mp3"
        config.temp_file_paths.append(temp_file_path)

    voice_part_provider.create_voice_part.side_effect = create_voice_part_success

    voice_line_file_name_provider_factory = Mock()
    voice_line_file_name_provider = Mock()
    voice_line_file_name_provider.provide_file_name.return_value = "final_output.mp3"
    voice_line_file_name_provider_factory.create_factory.return_value = (
        voice_line_file_name_provider
    )

    requests_manager = Mock()
    requests_manager.get_xtts_endpoint.return_value = "http://xtts_endpoint"

    filesystem_manager = Mock()
    filesystem_manager.get_temporary_folder_to_store_voice_parts.return_value = (
        "/temp_dir"
    )

    # Instantiate the algorithm
    algorithm = DirectVoiceLineGenerationAlgorithm(
        text=text,
        voice_part_provider_factory=voice_part_provider_factory,
        voice_line_file_name_provider_factory=voice_line_file_name_provider_factory,
        requests_manager=requests_manager,
        filesystem_manager=filesystem_manager,
    )

    # Run the method under test
    result = algorithm.direct_voice_line_generation()

    # Assertions
    assert result == "final_output.mp3"
    voice_line_file_name_provider.provide_file_name.assert_called_once()
