from typing import Dict

from src.dialogues.algorithms.update_summary_notes_algorithm import (
    UpdateSummaryNotesAlgorithm,
)


class UpdateSummaryNotesAlgorithmFactory:

    def __init__(self, summary_notes: Dict[str, Dict[str, Dict[str, str]]]):
        self._summary_notes = summary_notes

    def create_algorithm(
        self, speaker_identifier: str, new_summary_notes: Dict[str, Dict[str, str]]
    ) -> UpdateSummaryNotesAlgorithm:
        return UpdateSummaryNotesAlgorithm(
            speaker_identifier, self._summary_notes, new_summary_notes
        )
