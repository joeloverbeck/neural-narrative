from src.base.enums import TemplateType
from src.maps.algorithms.filter_out_used_templates_algorithm import (
    FilterOutUsedTemplatesAlgorithm,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory


class FilterOutUsedTemplatesAlgorithmFactory:

    def __init__(self, place_manager_factory: PlaceManagerFactory):
        self._place_manager_factory = place_manager_factory

    def create_factory(self, place_type: TemplateType):
        return FilterOutUsedTemplatesAlgorithm(place_type, self._place_manager_factory)
