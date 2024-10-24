class PlaythroughAlreadyExistsError(Exception):
    pass


class StoryUniverseTemplateNotFoundError(Exception):
    pass


class CharacterGenerationError(Exception):
    pass


class FailedToLoadJsonError(Exception):
    pass


class VoiceLineGenerationError(Exception):
    pass


class StoryUniverseGenerationError(Exception):
    pass


class NoEligibleWorldsError(Exception):
    pass
