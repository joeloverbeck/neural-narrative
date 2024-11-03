class DialogueProcessingError(Exception):
    pass


class InvalidNextSpeakerError(DialogueProcessingError):
    pass


class InvalidSpeechDataError(DialogueProcessingError):
    pass
