class TimeManager:
    def __init__(self, initial_time: float):
        if not isinstance(initial_time, float):
            raise ValueError(f"Expected 'initial_time' to be a float, but was {initial_time}")
        if initial_time >= 24:
            raise ValueError(f"Attempted to pass an invalid initial time to TimeManager: {initial_time}")

        self._world_time = initial_time

    def get_time_of_the_day(self):
        hour = int(self._world_time)

        if 6 <= hour < 12:
            return "in the morning"
        elif 12 <= hour < 18:
            return "in the afternoon"
        elif 18 <= hour < 22:
            return "in the evening"
        else:
            return "at night"

    def get_hour(self):
        return int(self._world_time)

    def advance_time(self, hours: int):
        self._world_time += hours
        if self._world_time >= 24:
            # Wrap around at 24 hours
            self._world_time -= 24
