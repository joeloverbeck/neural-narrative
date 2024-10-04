import random

from src.characters.characters_manager import CharactersManager
from src.maps.places_templates_parameter import PlacesTemplatesParameter


class CharacterGenerationInstructionsFormatter:

    def __init__(
        self,
        playthrough_name: str,
        location_name: str,
        location_description: str,
        templates: dict,
        places_templates_parameter: PlacesTemplatesParameter,
        characters_manager: CharactersManager = None,
    ):
        self._playthrough_name = playthrough_name
        self._location_name = location_name
        self._location_description = location_description
        self._templates = templates
        self._places_templates_parameter = places_templates_parameter

        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def format(
        self,
    ) -> str:
        """Formats the character generation instructions with the loaded templates and place parameters."""
        playthrough_metadata = self._templates["playthrough_metadata"]
        worlds_templates = self._templates["worlds_templates"]
        regions_templates = self._templates["regions_templates"]
        areas_templates = self._templates["areas_templates"]
        character_generation_instructions = self._templates[
            "character_generation_instructions"
        ]

        world_name = playthrough_metadata["world_template"]
        region_name = self._places_templates_parameter.get_region_template()
        area_name = self._places_templates_parameter.get_area_template()
        location_name = self._places_templates_parameter.get_location_template()

        key = self._characters_manager.create_key_for_character_generation_guidelines(
            world_name, region_name, area_name, location_name
        )

        if not self._characters_manager.are_there_character_generation_guidelines_for_place(
            world_name, region_name, area_name, location_name
        ):
            raise ValueError(
                f"No character generation guidelines exist for key '{key}'."
            )

        formatted_instructions = character_generation_instructions.format(
            world_name=world_name,
            world_description=worlds_templates[playthrough_metadata["world_template"]][
                "description"
            ],
            region_name=region_name,
            region_description=regions_templates[
                self._places_templates_parameter.get_region_template()
            ]["description"],
            area_name=area_name,
            area_description=areas_templates[
                self._places_templates_parameter.get_area_template()
            ]["description"],
            location_name=self._location_name,
            location_description=self._location_description,
            prohibited_names=self._characters_manager.get_all_character_names(),
            random_number=random.randint(-10, 10),
        )

        return formatted_instructions
