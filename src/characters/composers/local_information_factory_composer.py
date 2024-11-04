from src.base.validators import validate_non_empty_string
from src.maps.composers.get_current_weather_identifier_algorithm_composer import (
    GetCurrentWeatherIdentifierAlgorithmComposer,
)
from src.maps.factories.local_information_factory import LocalInformationFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.place_description_manager import PlaceDescriptionManager
from src.maps.templates_repository import TemplatesRepository
from src.maps.weathers_manager import WeathersManager


class LocalInformationFactoryComposer:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def compose_factory(self) -> LocalInformationFactory:
        weathers_manager = WeathersManager()

        place_manager_factory = PlaceManagerFactory(self._playthrough_name)

        template_repository = TemplatesRepository()

        place_description_manager = PlaceDescriptionManager(
            place_manager_factory, template_repository
        )

        get_current_weather_identifier_algorithm = (
            GetCurrentWeatherIdentifierAlgorithmComposer(
                self._playthrough_name
            ).compose_algorithm()
        )

        return LocalInformationFactory(
            self._playthrough_name,
            get_current_weather_identifier_algorithm,
            place_description_manager,
            weathers_manager,
        )
