from typing import List, Any, Optional

from src.maps.algorithms.structure_options_for_attaching_places_algorithm import (
    StructureOptionsForAttachingPlacesAlgorithm,
)


class StructureOptionsForAttachingPlacesAlgorithmFactory:

    @staticmethod
    def create_algorithm(
        items: List[Any],
        value_attr: Optional[str] = None,
        display_attr: Optional[str] = None,
    ) -> StructureOptionsForAttachingPlacesAlgorithm:
        return StructureOptionsForAttachingPlacesAlgorithm(
            items, value_attr, display_attr
        )
