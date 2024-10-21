from src.base.playthrough_manager import PlaythroughManager
from src.base.required_string import RequiredString


class TimeManager:

    def __init__(
        self,
        playthrough_name: RequiredString,
        playthrough_manager: PlaythroughManager = None,
    ):
        self._playthrough_name = playthrough_name

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def get_time_of_the_day(self) -> str:
        hour = self._playthrough_manager.get_hour()

        if 6 <= hour < 12:
            return "in the morning"
        elif 12 <= hour < 18:
            return "in the afternoon"
        elif 18 <= hour < 22:
            return "in the evening"
        else:
            return "at night"

    def get_hour(self) -> int:
        return int(self._playthrough_manager.get_hour())

    def advance_time(self, hours: int) -> None:
        hour = self._playthrough_manager.get_hour()

        hour += hours

        if hour >= 24:
            # Wrap around at 24 hours
            hour -= 24

        # Update the hour in the metadata
        self._playthrough_manager.update_hour(hour)
