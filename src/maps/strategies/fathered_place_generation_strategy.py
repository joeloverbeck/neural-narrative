from src.enums import TemplateType
from src.maps.abstracts.strategies import PlaceGenerationStrategy
from src.maps.commands.generate_place_command import GeneratePlaceCommand


class FatheredPlaceGenerationStrategy(PlaceGenerationStrategy):
    def __init__(
        self,
        place_template_type: TemplateType,
        father_place_name: str,
        notion: str = "",
    ):
        self._place_template_type = place_template_type
        self._father_place_name = father_place_name
        self._notion = notion

    def generate_place(self):
        father_template_type = {
            TemplateType.REGION: TemplateType.WORLD,
            TemplateType.AREA: TemplateType.REGION,
            TemplateType.LOCATION: TemplateType.AREA,
        }.get(self._place_template_type)

        if not father_template_type:
            raise ValueError(f"Invalid place type: {self._place_template_type}")

        # Generate the place using the provided parameters
        GeneratePlaceCommand(
            self._place_template_type,
            father_template_type,
            self._father_place_name,
            self._notion,
        ).execute()
