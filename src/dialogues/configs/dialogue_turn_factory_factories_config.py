from dataclasses import dataclass

from src.dialogues.factories.create_speech_turn_data_command_factory import (
    CreateSpeechTurnDataCommandFactory,
)
from src.dialogues.factories.summary_note_provider_factory import (
    SummaryNoteProviderFactory,
)
from src.dialogues.factories.update_summary_notes_algorithm_factory import (
    UpdateSummaryNotesAlgorithmFactory,
)


@dataclass
class DialogueTurnFactoryFactoriesConfig:
    summary_note_provider_factory: SummaryNoteProviderFactory
    create_speech_turn_data_command_factory: CreateSpeechTurnDataCommandFactory
    update_summary_notes_algorithm_factory: UpdateSummaryNotesAlgorithmFactory
