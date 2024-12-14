from src.base.playthrough_manager import PlaythroughManager
from src.time.exceptions import IncorrectHourError


class TimeManager:

    def __init__(
        self, playthrough_name: str, playthrough_manager: PlaythroughManager = None
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

    def set_hour(self, new_hour: int):
        if new_hour < 0 or new_hour >= 24:
            raise IncorrectHourError(
                f"Attempted to set new hour as '{new_hour}', which is not a valid hour."
            )

        self._playthrough_manager.update_hour(new_hour)

    def advance_time(self, hours: int) -> None:
        hour = self._playthrough_manager.get_hour()
        hour += hours
        if hour >= 24:
            hour -= 24
        self._playthrough_manager.update_hour(hour)
