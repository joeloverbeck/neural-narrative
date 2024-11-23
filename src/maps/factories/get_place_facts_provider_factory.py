from src.base.enums import TemplateType
from src.maps.factories.place_facts_provider_factory import PlaceFactsProviderFactory
from src.maps.providers.get_place_facts_provider import GetPlaceFactsProvider


class GetPlaceFactsProviderFactory:
    def __init__(self, place_facts_provider_factory: PlaceFactsProviderFactory):
        self._place_facts_provider_factory = place_facts_provider_factory

    def create_provider(
        self, place_template: str, place_description: str, place_type: TemplateType
    ) -> GetPlaceFactsProvider:
        return GetPlaceFactsProvider(
            place_template,
            place_description,
            place_type,
            self._place_facts_provider_factory,
        )
