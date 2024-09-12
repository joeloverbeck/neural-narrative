from src.dialogues.abstracts.abstract_factories import PlaceDataForDialoguePromptFactory
from src.dialogues.abstracts.factory_products import PlaceDataForDialoguePromptProduct
from src.dialogues.products.concrete_place_data_for_dialogue_prompt_product import \
    ConcretePlaceDataForDialoguePromptProduct
from src.enums import PlaceType
from src.maps.abstracts.factory_products import PlaceDataProduct
from src.maps.factories.concrete_current_place_factory import ConcreteCurrentPlaceFactory
from src.maps.factories.concrete_place_data_factory import ConcretePlaceDataFactory
from src.maps.maps import is_current_place_a_place_type, get_current_place_identifier
from src.maps.products.concrete_place_data_product import ConcretePlaceDataProduct


class ConcretePlaceDataForDialoguePromptFactory(PlaceDataForDialoguePromptFactory):

    def __init__(self, playthrough_name: str):
        assert playthrough_name

        self._playthrough_name = playthrough_name

    def _create_area_data(self, place_data_for_dialogue: dict, area_identifier: str) -> PlaceDataProduct:
        assert place_data_for_dialogue
        assert area_identifier

        # If at this point there's no location data in 'place_data_for_dialogue', we have a problem.
        if not place_data_for_dialogue["location_data"]:
            return ConcretePlaceDataProduct({}, is_valid=False,
                                            error="Attempted to create area data from location data, but the source dict didn't have location data.")

        # Every location is in an area, so must load that info too.
        area_data_product = ConcretePlaceDataFactory(self._playthrough_name,
                                                     place_data_for_dialogue["location_data"][
                                                         "area"]).create_place_data()

        return area_data_product

    def create_place_data_for_dialogue_prompt(self) -> PlaceDataForDialoguePromptProduct:
        place_data_for_dialogue = {
            "location_data": {},
            "area_data": {},
            "region_data": {}
        }

        if is_current_place_a_place_type(PlaceType.LOCATION, ConcreteCurrentPlaceFactory(self._playthrough_name)):
            location_data_product = ConcretePlaceDataFactory(self._playthrough_name, get_current_place_identifier(
                self._playthrough_name)).create_place_data()

            if not location_data_product.is_valid():
                return ConcretePlaceDataForDialoguePromptProduct({},
                                                                 is_valid=False,
                                                                 error=f"Location data product is invalid: {location_data_product.get_error()}")

            place_data_for_dialogue["location_data"] = location_data_product.get()

            create_area_data_result = self._create_area_data(place_data_for_dialogue,
                                                             place_data_for_dialogue["location_data"][
                                                                 "area"])

            if not create_area_data_result.is_valid():
                return ConcretePlaceDataForDialoguePromptProduct({}, is_valid=False,
                                                                 error=f"Was unable to create area data: {create_area_data_result.get_error()}")

            place_data_for_dialogue["area_data"] = create_area_data_result.get()

        else:
            # the current place is an area.
            create_area_data_result = self._create_area_data(place_data_for_dialogue,
                                                             get_current_place_identifier(self._playthrough_name))

            if not create_area_data_result.is_valid():
                return ConcretePlaceDataForDialoguePromptProduct({}, is_valid=False,
                                                                 error=f"Was unable to create area data: {create_area_data_result.get_error()}")

            place_data_for_dialogue["area_data"] = create_area_data_result.get()

        # In either case, we must also return the region data.
        region_data_product = ConcretePlaceDataFactory(self._playthrough_name,
                                                       place_data_for_dialogue["area_data"][
                                                           "region"]).create_place_data()

        if not region_data_product.is_valid():
            return ConcretePlaceDataForDialoguePromptProduct({}, is_valid=False,
                                                             error=f"Was unable to load the region data: {region_data_product.get_error()}")

        place_data_for_dialogue["region_data"] = region_data_product.get()

        return ConcretePlaceDataForDialoguePromptProduct(place_data_for_dialogue, is_valid=True)
