from typing import Optional


class PlacesTemplatesParameter:

    def __init__(
        self,
        world_template: str,
        region_template: str,
        area_template: str,
        location_template: Optional[str] = None,
        room_template: Optional[str] = None,
    ):
        self._world_template = world_template
        self._region_template = region_template
        self._area_template = area_template
        self._location_template = location_template
        self._room_template = room_template

    def get_world_template(self) -> str:
        return self._world_template

    def get_region_template(self) -> str:
        return self._region_template

    def get_area_template(self) -> str:
        return self._area_template

    def get_location_template(self) -> Optional[str]:
        return self._location_template

    def get_room_template(self) -> Optional[str]:
        return self._room_template
