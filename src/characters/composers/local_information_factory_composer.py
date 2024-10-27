from src.base.validators import validate_non_empty_string
from src.maps.factories.local_information_factory import LocalInformationFactory
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.place_description_manager import PlaceDescriptionManager
from src.maps.templates_repository import TemplatesRepository
from src.maps.weathers_manager import WeathersManager


class LocalInformationFactoryComposer:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def compose_factory(self) -> LocalInformationFactory:
        map_manager_factory = MapManagerFactory(self._playthrough_name)

        weathers_manager = WeathersManager(map_manager_factory)

        place_manager_factory = PlaceManagerFactory(self._playthrough_name)

        template_repository = TemplatesRepository()

        place_description_manager = PlaceDescriptionManager(
            place_manager_factory, template_repository
        )

        return LocalInformationFactory(
            self._playthrough_name, place_description_manager, weathers_manager
        )
