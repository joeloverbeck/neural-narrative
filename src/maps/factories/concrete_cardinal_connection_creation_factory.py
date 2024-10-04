from src.enums import PlaceType
from src.maps.abstracts.abstract_factories import CardinalConnectionCreationFactory
from src.maps.abstracts.factory_products import CardinalConnectionCreationProduct
from src.maps.enums import RandomPlaceTypeMapEntryCreationResultType, CardinalDirection
from src.maps.factories.concrete_random_place_template_based_on_categories_factory import (
    ConcreteRandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.factories.concrete_random_place_type_map_entry_creation_factory import (
    ConcreteRandomPlaceTypeMapEntryCreationFactory,
)
from src.maps.factories.create_map_entry_for_playthrough_command_factory import (
    CreateMapEntryForPlaythroughCommandFactory,
)
from src.maps.map_manager import MapManager
from src.maps.products.concrete_cardinal_connection_creation_product import (
    ConcreteCardinalConnectionCreationProduct,
)
from src.playthrough_manager import PlaythroughManager


class ConcreteCardinalConnectionCreationFactory(CardinalConnectionCreationFactory):

    def __init__(
        self,
        playthrough_name: str,
        cardinal_direction: CardinalDirection,
        map_manager: MapManager = None,
        playthrough_manager: PlaythroughManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._cardinal_direction = cardinal_direction

        self._map_manager = map_manager or MapManager(self._playthrough_name)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def create_cardinal_connection(self) -> CardinalConnectionCreationProduct:
        father_template = self._map_manager.get_father_template()

        random_place_template_based_on_categories_factory = (
            ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(self._playthrough_name)
        )

        create_map_entry_for_playthrough_command_factory = (
            CreateMapEntryForPlaythroughCommandFactory(
                self._playthrough_name,
                self._map_manager.get_father_identifier(
                    self._playthrough_manager.get_current_place_identifier()
                ),
                PlaceType.AREA,
            )
        )

        result = ConcreteRandomPlaceTypeMapEntryCreationFactory(
            self._playthrough_name,
            father_template,
            PlaceType.AREA,
            PlaceType.REGION,
            random_place_template_based_on_categories_factory,
            create_map_entry_for_playthrough_command_factory,
        ).create_random_place_type_map_entry()

        if (
            result.get_result_type()
            == RandomPlaceTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
        ):
            return ConcreteCardinalConnectionCreationProduct(
                was_successful=False, error="No remaining areas to add to map."
            )

        if (
            result.get_result_type()
            == RandomPlaceTypeMapEntryCreationResultType.FAILURE
        ):
            return ConcreteCardinalConnectionCreationProduct(
                was_successful=False,
                error=f"Couldn't add an area {self._cardinal_direction.value}: {result.get_error()}",
            )

        new_id, _ = (
            self._map_manager.get_identifier_and_place_template_of_latest_map_entry()
        )

        # All correct. Must add the newly created map entry as one of the cardinal connections to the current place.
        self._map_manager.create_cardinal_connection(
            self._cardinal_direction,
            self._playthrough_manager.get_current_place_identifier(),
            new_id,
        )

        # After you create the cardinal connection in origin, you must create the opposite cardinal connection in the destination.
        opposite_cardinal_direction = self._map_manager.get_opposite_cardinal_direction(
            self._cardinal_direction
        )

        self._map_manager.create_cardinal_connection(
            opposite_cardinal_direction,
            new_id,
            self._playthrough_manager.get_current_place_identifier(),
        )

        return ConcreteCardinalConnectionCreationProduct(was_successful=True)
