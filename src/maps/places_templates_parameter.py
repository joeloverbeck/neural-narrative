from typing import Optional


class PlacesTemplatesParameter:
    def __init__(self, region_template: str, area_template: str,
                 location_template: Optional[str] = None):
        assert region_template
        assert area_template

        self._region_template = region_template
        self._area_template = area_template
        self._location_template = location_template

    def get_region_template(self) -> str:
        return self._region_template

    def get_area_template(self) -> str:
        return self._area_template

    def get_location_template(self) -> Optional[str]:
        return self._location_template
