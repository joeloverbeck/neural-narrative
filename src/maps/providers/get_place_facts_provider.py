from typing import Dict, Optional

from src.base.enums import TemplateType
from src.base.validators import validate_non_empty_string
from src.maps.factories.place_facts_provider_factory import PlaceFactsProviderFactory
from src.maps.models.place_facts import PlaceFacts
from src.maps.repositories.places_facts_repository import PlacesFactsRepository


class GetPlaceFactsProvider:

    def __init__(
        self,
        place_template: str,
        place_description: str,
        place_type: TemplateType,
        place_facts_provider_factory: PlaceFactsProviderFactory,
        places_facts_repository: Optional[PlacesFactsRepository] = None,
    ):
        validate_non_empty_string(place_template, "place_template")
        validate_non_empty_string(place_description, "place_description")

        self._place_template = place_template
        self._place_description = place_description
        self._place_type = place_type
        self._place_facts_provider_factory = place_facts_provider_factory

        self._places_facts_repository = (
            places_facts_repository or PlacesFactsRepository()
        )

    def get_place_facts(self) -> Dict[str, str]:
        place_facts = self._places_facts_repository.get_place_facts(
            self._place_template, self._place_type
        )

        if place_facts:
            return place_facts

        # At this point, there weren't place facts, so we must generate them.
        product = self._place_facts_provider_factory.create_provider(
            self._place_description
        ).generate_product(PlaceFacts)

        # Store the facts.
        self._places_facts_repository.set_place_facts(
            self._place_template, product.get(), self._place_type
        )

        return product.get()
