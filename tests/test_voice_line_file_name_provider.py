import logging
from unittest.mock import MagicMock, patch

from src.base.required_string import RequiredString
from src.voices.providers.voice_line_file_name_provider import VoiceLineFileNameProvider


# Test initialization with valid parameters
def test_init_valid_parameters():
    character_name = RequiredString("Test Character")
    voice_model = RequiredString("Test Voice Model")
    temp_dir = RequiredString("/tmp/test_dir")
    temp_file_paths = [
        RequiredString("/tmp/test_dir/file1.wav"),
        RequiredString("/tmp/test_dir/file2.wav"),
    ]
    voice_manager = MagicMock()
    filesystem_manager = MagicMock()

    provider = VoiceLineFileNameProvider(
        character_name,
        voice_model,
        temp_dir,
        temp_file_paths,
        voice_manager,
        filesystem_manager,
    )

    assert provider._character_name == character_name
    assert provider._voice_model == voice_model
    assert provider._temp_dir == temp_dir
    assert provider._temp_file_paths == temp_file_paths
    assert provider._voice_manager == voice_manager
    assert provider._filesystem_manager == filesystem_manager


# Test provide_file_name calls get_file_path_for_voice_line
def test_provide_file_name_calls_get_file_path_for_voice_line():
    character_name = RequiredString("Test Character")
    voice_model = RequiredString("Test Voice Model")
    temp_file_paths = [RequiredString("file1.wav"), RequiredString("file2.wav")]
    filesystem_manager = MagicMock()
    filesystem_manager.get_file_path_for_voice_line.return_value = "final.wav"
    provider = VoiceLineFileNameProvider(
        character_name,
        voice_model,
        RequiredString("temp_dir"),
        temp_file_paths,
        MagicMock(),
        filesystem_manager=filesystem_manager,
    )

    with patch("os.remove"), patch("os.rmdir"):
        provider.provide_file_name()

    filesystem_manager.get_file_path_for_voice_line.assert_called_once_with(
        character_name, voice_model
    )


# Test provide_file_name calls concatenate_wav_files_from_list
def test_provide_file_name_calls_concatenate_wav_files():
    temp_file_paths = [RequiredString("file1.wav"), RequiredString("file2.wav")]
    voice_manager = MagicMock()
    filesystem_manager = MagicMock()
    filesystem_manager.get_file_path_for_voice_line.return_value = "final.wav"
    provider = VoiceLineFileNameProvider(
        RequiredString("character_name"),
        RequiredString("voice_model"),
        RequiredString("temp_dir"),
        temp_file_paths,
        voice_manager,
        filesystem_manager,
    )

    with patch("os.remove"), patch("os.rmdir"):
        provider.provide_file_name()

    voice_manager.concatenate_wav_files_from_list.assert_called_once_with(
        temp_file_paths, "final.wav"
    )


# Test provide_file_name removes temp directory
def test_provide_file_name_removes_temp_dir():
    voice_manager = MagicMock()
    filesystem_manager = MagicMock()
    filesystem_manager.get_file_path_for_voice_line.return_value = "final.wav"
    provider = VoiceLineFileNameProvider(
        RequiredString("character_name"),
        RequiredString("voice_model"),
        RequiredString("temp_dir"),
        [RequiredString("file1.wav")],
        voice_manager,
        filesystem_manager,
    )

    with patch("os.remove"), patch("os.rmdir") as mock_rmdir, patch("shutil.copy"):
        provider.provide_file_name()

    mock_rmdir.assert_called_once_with("temp_dir")


# Test provide_file_name returns file name
def test_provide_file_name_returns_file_name():
    voice_manager = MagicMock()
    filesystem_manager = MagicMock()
    filesystem_manager.get_file_path_for_voice_line.return_value = "final.wav"
    provider = VoiceLineFileNameProvider(
        RequiredString("character_name"),
        RequiredString("voice_model"),
        RequiredString("temp_dir"),
        [RequiredString("file1.wav")],
        voice_manager,
        filesystem_manager,
    )

    with patch("os.remove"), patch("os.rmdir"), patch("shutil.copy"):
        result = provider.provide_file_name()

    assert result == RequiredString("final.wav")


# Test provide_file_name continues after os.remove exception
def test_provide_file_name_continues_after_remove_exception(caplog):
    caplog.set_level(logging.WARNING)
    temp_file_paths = [RequiredString("file1.wav"), RequiredString("file2.wav")]
    voice_manager = MagicMock()
    filesystem_manager = MagicMock()
    filesystem_manager.get_file_path_for_voice_line.return_value = "final.wav"
    provider = VoiceLineFileNameProvider(
        RequiredString("character_name"),
        RequiredString("voice_model"),
        RequiredString("temp_dir"),
        temp_file_paths,
        voice_manager,
        filesystem_manager,
    )

    def side_effect(path):
        if path == "file1.wav":
            raise Exception("Remove error")

    with patch("os.remove", side_effect=side_effect) as mock_remove, patch("os.rmdir"):
        result = provider.provide_file_name()

    assert result == RequiredString("final.wav")
    assert mock_remove.call_count == 2
    assert "Error removing temporary file file1.wav: Remove error" in caplog.text
