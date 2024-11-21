import logging
from typing import Dict

from src.base.tools import is_convertible_to_int
from src.base.validators import validate_non_empty_string

logger = logging.getLogger(__name__)


class UpdateSummaryNotesAlgorithm:

    def __init__(
        self,
        speaker_identifier: str,
        summary_notes: Dict[str, Dict[str, Dict[str, str]]],
        new_summary_notes: Dict[str, Dict[str, str]],
    ):
        validate_non_empty_string(speaker_identifier, "speaker_identifier")

        self._speaker_identifier = speaker_identifier
        self._summary_notes = summary_notes
        self._new_summary_notes = new_summary_notes

    def do_algorithm(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        # Get the existing notes for the speaker identifier, or initialize an empty dict
        previous_summary_notes = self._summary_notes.get(self._speaker_identifier, {})

        # Update the previous notes with new notes
        for key, value in self._new_summary_notes.items():
            if key in previous_summary_notes:
                previous_summary_notes[key].update(value)
            else:
                previous_summary_notes[key] = value

        # Update the summary_notes with the updated notes for the speaker
        self._summary_notes[self._speaker_identifier] = previous_summary_notes

        # Ensure all outer keys are convertible to int
        for key in self._summary_notes.keys():
            convertible, _ = is_convertible_to_int(key)
            if not convertible:
                raise ValueError(f"The key '{key}' is not convertible to int.")

        return self._summary_notes
