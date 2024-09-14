from typing import Protocol

from src.abstracts.subject import Subject
from src.dialogues.abstracts.strategies import InvolvePlayerInDialogueStrategy


class InvolvePlayerInDialogueStrategySubject(InvolvePlayerInDialogueStrategy, Subject, Protocol):
    pass
