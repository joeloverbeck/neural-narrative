from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.templates_repository import TemplatesRepository


class PlaceDescriptionManager:

    def __init__(self, place_manager_factory: PlaceManagerFactory,
                 template_repository: TemplatesRepository):
        self._place_manager_factory = place_manager_factory
        self._template_repository = template_repository

    def get_place_description(self, place_identifier: str) -> str:
        place = self._place_manager_factory.create_place_manager().get_place(
            place_identifier)
        place_type = self._place_manager_factory.create_place_manager(
        ).determine_place_type(place_identifier)
        templates = self._template_repository.load_template(place_type)
        place_template = place.get('place_template')
        template_data = templates.get(place_template)
        if not template_data:
            raise ValueError(f"Template '{place_template}' not found.")
        place_description = template_data.get('description')
        if not place_description:
            raise ValueError(
                f"The description for place '{place_identifier}' was empty.")
        return place_description
