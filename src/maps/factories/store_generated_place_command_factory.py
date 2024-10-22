from src.base.enums import TemplateType
from src.maps.commands.store_generated_place_command import StoreGeneratedPlaceCommand
from src.maps.place_data import PlaceData


class StoreGeneratedPlaceCommandFactory:

    def __init__(self, place_template_type: TemplateType):
        self._place_template_type = place_template_type

    def create_command(self, place_data: PlaceData
                       ) -> StoreGeneratedPlaceCommand:
        return StoreGeneratedPlaceCommand(place_data, self._place_template_type
                                          )
