from enum import Enum, auto


class HandleDialogueStateAlgorithmResultType(Enum):
    CONTINUE = auto()
    SHOULD_REDIRECT_TO_PARTICIPANTS = auto()
