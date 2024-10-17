class PlaythroughAlreadyExistsError(Exception):
    pass


class WorldTemplateNotFoundError(Exception):
    pass


class CharacterGenerationError(Exception):
    pass


class FailedToLoadJsonError(Exception):
    pass


class VoiceLineGenerationError(Exception):
    pass


class PlotBlueprintGenerationError(Exception):
    pass
