from src.dialogues.abstracts.abstract_factories import PlaceDataForDialoguePromptFactory
from src.dialogues.abstracts.factory_products import PlaceDataForDialoguePromptProduct
from src.dialogues.products.concrete_place_data_for_dialogue_prompt_product import \
    ConcretePlaceDataForDialoguePromptProduct
from src.maps.abstracts.abstract_factories import CurrentLocationDataFactory
from src.maps.factories.concrete_area_data_factory import ConcreteAreaDataFactory
from src.maps.maps import is_current_place_a_location


class ConcretePlaceDataForDialoguePromptFactory(PlaceDataForDialoguePromptFactory):

    def __init__(self, playthrough_name: str, current_location_data_factory: CurrentLocationDataFactory):
        assert playthrough_name
        assert current_location_data_factory

        self._playthrough_name = playthrough_name
        self._current_location_data_factory = current_location_data_factory

    def create_place_data_for_dialogue_prompt(self) -> PlaceDataForDialoguePromptProduct:
        place_data_for_dialogue = {
            "location_data": None,
            "area_data": None
        }

        if is_current_place_a_location(self._playthrough_name):
            current_location_data_product = self._current_location_data_factory.create_current_location_data()

            if not current_location_data_product.is_valid():
                return ConcretePlaceDataForDialoguePromptProduct({},
                                                                 is_valid=False,
                                                                 error=f"Current location data product is invalid: {current_location_data_product.get_error()}")

            place_data_for_dialogue["location_data"] = current_location_data_product.get()

            # Every location is in an area, so must load that info too.
            area_data_product = ConcreteAreaDataFactory(self._playthrough_name,
                                                        place_data_for_dialogue["location_data"][
                                                            "area"]).create_area_data()

            if not area_data_product.is_valid():
                return ConcretePlaceDataForDialoguePromptProduct({}, is_valid=False,
                                                                 error=f"Wasn't able to produce valid area data: {area_data_product.get_error()}")

            # The area product is valid, so store it in the place data for dialogue
            place_data_for_dialogue["area_data"] = area_data_product.get()

        return ConcretePlaceDataForDialoguePromptProduct(place_data_for_dialogue, is_valid=True)
