import pytest

from src.dialogues.algorithms.update_summary_notes_algorithm import (
    UpdateSummaryNotesAlgorithm,
)


# Test cases
def test_valid_update_with_existing_notes():
    speaker_identifier = "1"
    summary_notes = {"1": {"session1": {"note1": "content1"}}}
    new_summary_notes = {
        "session1": {"note2": "content2"},
        "session2": {"note3": "content3"},
    }
    expected_output = {
        "1": {
            "session1": {"note1": "content1", "note2": "content2"},
            "session2": {"note3": "content3"},
        }
    }
    algorithm = UpdateSummaryNotesAlgorithm(
        speaker_identifier, summary_notes, new_summary_notes
    )
    assert algorithm.do_algorithm() == expected_output


def test_valid_update_without_existing_notes():
    speaker_identifier = "2"
    summary_notes = {}
    new_summary_notes = {"session1": {"note1": "content1"}}
    expected_output = {"2": {"session1": {"note1": "content1"}}}
    algorithm = UpdateSummaryNotesAlgorithm(
        speaker_identifier, summary_notes, new_summary_notes
    )
    assert algorithm.do_algorithm() == expected_output


def test_empty_speaker_identifier():
    with pytest.raises(ValueError) as excinfo:
        UpdateSummaryNotesAlgorithm("", {}, {})
    assert "speaker_identifier" in str(excinfo.value)


def test_key_not_convertible_to_int_in_summary_notes():
    speaker_identifier = "3"
    summary_notes = {"not_an_int": {"session1": {"note1": "content1"}}}
    new_summary_notes = {}
    algorithm = UpdateSummaryNotesAlgorithm(
        speaker_identifier, summary_notes, new_summary_notes
    )
    with pytest.raises(ValueError) as excinfo:
        algorithm.do_algorithm()
    assert "not convertible to int" in str(excinfo.value)


def test_key_not_convertible_to_int_after_update():
    speaker_identifier = "4"
    summary_notes = {"4": {"session1": {"note1": "content1"}}}
    new_summary_notes = {}
    algorithm = UpdateSummaryNotesAlgorithm(
        speaker_identifier, summary_notes, new_summary_notes
    )
    # Manually inject an invalid key
    algorithm._summary_notes["invalid_key"] = {}
    with pytest.raises(ValueError) as excinfo:
        algorithm.do_algorithm()
    assert "not convertible to int" in str(excinfo.value)


def test_update_with_empty_new_summary_notes():
    speaker_identifier = "5"
    summary_notes = {"5": {"session1": {"note1": "content1"}}}
    new_summary_notes = {}
    expected_output = summary_notes.copy()
    algorithm = UpdateSummaryNotesAlgorithm(
        speaker_identifier, summary_notes, new_summary_notes
    )
    assert algorithm.do_algorithm() == expected_output


def test_update_returns_correct_structure():
    speaker_identifier = "6"
    summary_notes = {}
    new_summary_notes = {"session1": {"note1": "content1", "note2": "content2"}}
    expected_output = {"6": {"session1": {"note1": "content1", "note2": "content2"}}}
    algorithm = UpdateSummaryNotesAlgorithm(
        speaker_identifier, summary_notes, new_summary_notes
    )
    assert algorithm.do_algorithm() == expected_output


def test_invalid_speaker_identifier_not_convertible_to_int():
    speaker_identifier = "non_int"
    summary_notes = {}
    new_summary_notes = {}
    algorithm = UpdateSummaryNotesAlgorithm(
        speaker_identifier, summary_notes, new_summary_notes
    )
    with pytest.raises(ValueError) as excinfo:
        algorithm.do_algorithm()
    assert "not convertible to int" in str(excinfo.value)


def test_valid_speaker_identifier_convertible_to_int():
    speaker_identifier = "8"
    summary_notes = {}
    new_summary_notes = {}
    algorithm = UpdateSummaryNotesAlgorithm(
        speaker_identifier, summary_notes, new_summary_notes
    )
    try:
        algorithm.do_algorithm()
    except ValueError:
        pytest.fail("do_algorithm raised ValueError unexpectedly!")
