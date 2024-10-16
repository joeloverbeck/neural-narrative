import logging
from unittest.mock import MagicMock, patch

import pytest

from src.voices.providers.voice_line_file_name_provider import VoiceLineFileNameProvider


# Test initialization with valid parameters
def test_init_valid_parameters():
    character_name = "Test Character"
    voice_model = "Test Voice Model"
    temp_dir = "/tmp/test_dir"
    temp_file_paths = ["/tmp/test_dir/file1.wav", "/tmp/test_dir/file2.wav"]
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


# Test initialization with empty character_name
def test_init_empty_character_name():
    with pytest.raises(ValueError) as exc_info:
        VoiceLineFileNameProvider("", "voice_model", "temp_dir", ["file1.wav"])
    assert str(exc_info.value) == "character_name can't be empty."


# Test initialization with empty voice_model
def test_init_empty_voice_model():
    with pytest.raises(ValueError) as exc_info:
        VoiceLineFileNameProvider("character_name", "", "temp_dir", ["file1.wav"])
    assert str(exc_info.value) == "voice_model can't be empty."


# Test initialization with empty temp_dir
def test_init_empty_temp_dir():
    with pytest.raises(ValueError) as exc_info:
        VoiceLineFileNameProvider("character_name", "voice_model", "", ["file1.wav"])
    assert str(exc_info.value) == "temp_dir can't be empty."


# Test initialization with empty temp_file_paths
def test_init_empty_temp_file_paths():
    with pytest.raises(ValueError) as exc_info:
        VoiceLineFileNameProvider("character_name", "voice_model", "temp_dir", [])
    assert str(exc_info.value) == "temp_file_paths can't be empty."


# Test provide_file_name calls get_file_path_for_voice_line
def test_provide_file_name_calls_get_file_path_for_voice_line():
    character_name = "Test Character"
    voice_model = "Test Voice Model"
    temp_file_paths = ["file1.wav", "file2.wav"]
    filesystem_manager = MagicMock()
    filesystem_manager.get_file_path_for_voice_line.return_value = "final.wav"
    provider = VoiceLineFileNameProvider(
        character_name,
        voice_model,
        "temp_dir",
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
    temp_file_paths = ["file1.wav", "file2.wav"]
    voice_manager = MagicMock()
    filesystem_manager = MagicMock()
    filesystem_manager.get_file_path_for_voice_line.return_value = "final.wav"
    provider = VoiceLineFileNameProvider(
        "character_name",
        "voice_model",
        "temp_dir",
        temp_file_paths,
        voice_manager,
        filesystem_manager,
    )

    with patch("os.remove"), patch("os.rmdir"):
        provider.provide_file_name()

    voice_manager.concatenate_wav_files_from_list.assert_called_once_with(
        temp_file_paths, "final.wav"
    )


# Test provide_file_name removes temp files
def test_provide_file_name_removes_temp_files():
    temp_file_paths = ["file1.wav", "file2.wav"]
    voice_manager = MagicMock()
    filesystem_manager = MagicMock()
    filesystem_manager.get_file_path_for_voice_line.return_value = "final.wav"
    provider = VoiceLineFileNameProvider(
        "character_name",
        "voice_model",
        "temp_dir",
        temp_file_paths,
        voice_manager,
        filesystem_manager,
    )

    with patch("os.remove") as mock_remove, patch("os.rmdir"):
        provider.provide_file_name()

    expected_calls = [((path,),) for path in temp_file_paths]
    assert mock_remove.call_args_list == expected_calls


# Test provide_file_name removes temp directory
def test_provide_file_name_removes_temp_dir():
    voice_manager = MagicMock()
    filesystem_manager = MagicMock()
    filesystem_manager.get_file_path_for_voice_line.return_value = "final.wav"
    provider = VoiceLineFileNameProvider(
        "character_name",
        "voice_model",
        "temp_dir",
        ["file1.wav"],
        voice_manager,
        filesystem_manager,
    )

    with patch("os.remove"), patch("os.rmdir") as mock_rmdir:
        provider.provide_file_name()

    mock_rmdir.assert_called_once_with("temp_dir")


# Test provide_file_name returns file name
def test_provide_file_name_returns_file_name():
    voice_manager = MagicMock()
    filesystem_manager = MagicMock()
    filesystem_manager.get_file_path_for_voice_line.return_value = "final.wav"
    provider = VoiceLineFileNameProvider(
        "character_name",
        "voice_model",
        "temp_dir",
        ["file1.wav"],
        voice_manager,
        filesystem_manager,
    )

    with patch("os.remove"), patch("os.rmdir"):
        result = provider.provide_file_name()

    assert result == "final.wav"


# Test provide_file_name handles exception in concatenate_wav_files_from_list
def test_provide_file_name_handles_concatenate_exception(caplog):
    caplog.set_level(logging.ERROR)
    voice_manager = MagicMock()
    voice_manager.concatenate_wav_files_from_list.side_effect = Exception(
        "Concatenate error"
    )
    filesystem_manager = MagicMock()
    provider = VoiceLineFileNameProvider(
        "character_name",
        "voice_model",
        "temp_dir",
        ["file1.wav"],
        voice_manager,
        filesystem_manager,
    )

    result = provider.provide_file_name()

    assert result is None
    assert "Error concatenating voice lines: Concatenate error" in caplog.text


# Test provide_file_name handles exception in os.remove
def test_provide_file_name_handles_remove_exception(caplog):
    caplog.set_level(logging.WARNING)
    voice_manager = MagicMock()
    filesystem_manager = MagicMock()
    provider = VoiceLineFileNameProvider(
        "character_name",
        "voice_model",
        "temp_dir",
        ["file1.wav"],
        voice_manager,
        filesystem_manager,
    )

    with patch("os.remove", side_effect=Exception("Remove error")):
        with patch("os.rmdir"):
            provider.provide_file_name()

    assert "Error removing temporary file file1.wav: Remove error" in caplog.text


# Test provide_file_name handles exception in os.rmdir
def test_provide_file_name_handles_rmdir_exception(caplog):
    caplog.set_level(logging.WARNING)
    voice_manager = MagicMock()
    filesystem_manager = MagicMock()
    provider = VoiceLineFileNameProvider(
        "character_name",
        "voice_model",
        "temp_dir",
        ["file1.wav"],
        voice_manager,
        filesystem_manager,
    )

    with patch("os.remove"), patch("os.rmdir", side_effect=OSError("Rmdir error")):
        provider.provide_file_name()

    assert "Error removing temporary directory temp_dir: Rmdir error" in caplog.text


# Test provide_file_name continues after os.remove exception
def test_provide_file_name_continues_after_remove_exception(caplog):
    caplog.set_level(logging.WARNING)
    temp_file_paths = ["file1.wav", "file2.wav"]
    voice_manager = MagicMock()
    filesystem_manager = MagicMock()
    filesystem_manager.get_file_path_for_voice_line.return_value = "final.wav"
    provider = VoiceLineFileNameProvider(
        "character_name",
        "voice_model",
        "temp_dir",
        temp_file_paths,
        voice_manager,
        filesystem_manager,
    )

    def side_effect(path):
        if path == "file1.wav":
            raise Exception("Remove error")

    with patch("os.remove", side_effect=side_effect) as mock_remove, patch("os.rmdir"):
        result = provider.provide_file_name()

    assert result == "final.wav"
    assert mock_remove.call_count == 2
    assert "Error removing temporary file file1.wav: Remove error" in caplog.text


# Test provide_file_name when temp_file_paths is None
def test_init_none_temp_file_paths():
    with pytest.raises(ValueError) as exc_info:
        VoiceLineFileNameProvider("character_name", "voice_model", "temp_dir", None)
    assert str(exc_info.value) == "temp_file_paths can't be empty."
