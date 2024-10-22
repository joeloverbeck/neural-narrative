from unittest.mock import Mock, patch
from src.base.exceptions import VoiceLineGenerationError
from src.voices.algorithms.direct_voice_line_generation_algorithm import (
    DirectVoiceLineGenerationAlgorithm,
)


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


@patch("time.strftime", return_value="20220101010101")
def test_direct_voice_line_generation_processes_each_part(mock_strftime):
    text = "This is *emphasized* text."
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
    (filesystem_manager.get_temporary_folder_to_store_voice_parts.return_value) = (
        "/temp_dir"
    )

    def create_voice_part_side_effect():
        config = voice_part_provider_factory.create_provider.call_args_list[-1][0][0]
        file_path = f"{config.temp_dir}/part{config.index}.mp3"
        config.temp_file_paths.append(file_path)

    voice_part_provider.create_voice_part.side_effect = create_voice_part_side_effect
    algorithm = DirectVoiceLineGenerationAlgorithm(
        text=text,
        voice_part_provider_factory=voice_part_provider_factory,
        voice_line_file_name_provider_factory=voice_line_file_name_provider_factory,
        requests_manager=requests_manager,
        filesystem_manager=filesystem_manager,
    )
    result = algorithm.direct_voice_line_generation()
    expected_parts = ["This is ", "*emphasized*", " text."]
    assert voice_part_provider_factory.create_provider.call_count == len(expected_parts)
    assert voice_part_provider.create_voice_part.call_count == len(expected_parts)
    assert result == "output_file.mp3"
    calls = voice_part_provider_factory.create_provider.call_args_list
    for index, call in enumerate(calls):
        args, _ = call
        config = args[0]
        assert config.part == expected_parts[index]
        assert config.xtts_endpoint == "http://xtts_endpoint"
        assert config.timestamp == "20220101010101"
        assert config.index == index
        assert config.temp_dir == "/temp_dir"
    expected_temp_file_paths = [
        "/temp_dir/part0.mp3",
        "/temp_dir/part1.mp3",
        "/temp_dir/part2.mp3",
    ]
    assert config.temp_file_paths == expected_temp_file_paths
    voice_line_file_name_provider_factory.create_factory.assert_called_once_with(
        "/temp_dir", expected_temp_file_paths
    )
    voice_line_file_name_provider.provide_file_name.assert_called_once()


@patch("time.strftime", return_value="20220101010101")
def test_direct_voice_line_generation_no_voice_lines_generated(mock_strftime):
    text = "Sample text with no voice lines generated."
    voice_part_provider_factory = Mock()
    voice_part_provider = Mock()
    voice_part_provider_factory.create_provider.return_value = voice_part_provider

    def create_voice_part_noop():
        pass

    voice_part_provider.create_voice_part.side_effect = create_voice_part_noop
    voice_line_file_name_provider_factory = Mock()
    voice_line_file_name_provider_factory.create_factory.return_value = Mock()
    requests_manager = Mock()
    requests_manager.get_xtts_endpoint.return_value = "http://xtts_endpoint"
    filesystem_manager = Mock()
    (filesystem_manager.get_temporary_folder_to_store_voice_parts.return_value) = (
        "/temp_dir"
    )
    algorithm = DirectVoiceLineGenerationAlgorithm(
        text=text,
        voice_part_provider_factory=voice_part_provider_factory,
        voice_line_file_name_provider_factory=voice_line_file_name_provider_factory,
        requests_manager=requests_manager,
        filesystem_manager=filesystem_manager,
    )
    result = algorithm.direct_voice_line_generation()
    assert result is None


@patch("time.strftime", return_value="20220101010101")
def test_direct_voice_line_generation_handles_exceptions(mock_strftime):
    text = "Part one. *Part two with error*. Part three."
    voice_part_provider_factory = Mock()
    voice_part_provider = Mock()
    voice_part_provider_factory.create_provider.return_value = voice_part_provider
    temp_file_paths = []

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
    (filesystem_manager.get_temporary_folder_to_store_voice_parts.return_value) = (
        "/temp_dir"
    )
    algorithm = DirectVoiceLineGenerationAlgorithm(
        text=text,
        voice_part_provider_factory=voice_part_provider_factory,
        voice_line_file_name_provider_factory=voice_line_file_name_provider_factory,
        requests_manager=requests_manager,
        filesystem_manager=filesystem_manager,
    )
    result = algorithm.direct_voice_line_generation()
    expected_temp_file_paths = ["/temp_dir/part0.mp3", "/temp_dir/part2.mp3"]
    assert result == "output_file.mp3"
    config_calls = voice_part_provider_factory.create_provider.call_args_list
    final_temp_file_paths = config_calls[0][0][0].temp_file_paths
    assert final_temp_file_paths == expected_temp_file_paths
    assert voice_part_provider.create_voice_part.call_count == 3


@patch("time.strftime", return_value="20220101010101")
def test_direct_voice_line_generation_calls_provide_file_name(mock_strftime):
    text = "Generate voice lines for this text."
    voice_part_provider_factory = Mock()
    voice_part_provider = Mock()
    voice_part_provider_factory.create_provider.return_value = voice_part_provider

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
    (filesystem_manager.get_temporary_folder_to_store_voice_parts.return_value) = (
        "/temp_dir"
    )
    algorithm = DirectVoiceLineGenerationAlgorithm(
        text=text,
        voice_part_provider_factory=voice_part_provider_factory,
        voice_line_file_name_provider_factory=voice_line_file_name_provider_factory,
        requests_manager=requests_manager,
        filesystem_manager=filesystem_manager,
    )
    result = algorithm.direct_voice_line_generation()
    assert result == "final_output.mp3"
    voice_line_file_name_provider.provide_file_name.assert_called_once()
