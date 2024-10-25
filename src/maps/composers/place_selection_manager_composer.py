from src.base.validators import validate_non_empty_string
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.place_selection_manager import PlaceSelectionManager
from src.maps.templates_repository import TemplatesRepository


class PlaceSelectionManagerComposer:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def compose_manager(self) -> PlaceSelectionManager:
        place_manager_factory = PlaceManagerFactory(self._playthrough_name)
        template_repository = TemplatesRepository()
        return PlaceSelectionManager(place_manager_factory, template_repository)
