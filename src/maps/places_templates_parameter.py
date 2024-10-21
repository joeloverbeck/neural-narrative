from typing import Optional

from src.base.required_string import RequiredString


class PlacesTemplatesParameter:
    def __init__(
        self,
        world_template: RequiredString,
        region_template: RequiredString,
        area_template: RequiredString,
        location_template: Optional[RequiredString] = None,
    ):
        self._world_template = world_template
        self._region_template = region_template
        self._area_template = area_template
        self._location_template = location_template

    def get_world_template(self) -> RequiredString:
        return self._world_template

    def get_region_template(self) -> RequiredString:
        return self._region_template

    def get_area_template(self) -> RequiredString:
        return self._area_template

    def get_location_template(self) -> Optional[RequiredString]:
        return self._location_template
