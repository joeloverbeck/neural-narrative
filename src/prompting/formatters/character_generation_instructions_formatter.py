import random
from typing import Optional

from src.characters.character_guidelines_manager import CharacterGuidelinesManager
from src.characters.characters_manager import CharactersManager
from src.maps.places_templates_parameter import PlacesTemplatesParameter


class CharacterGenerationInstructionsFormatter:

    def __init__(
        self,
        playthrough_name: str,
        places_descriptions: str,
        templates: dict,
        places_templates_parameter: PlacesTemplatesParameter,
        character_guidelines_manager: Optional[CharacterGuidelinesManager] = None,
        characters_manager: Optional[CharactersManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._places_descriptions = places_descriptions
        self._templates = templates
        self._places_templates_parameter = places_templates_parameter

        self._character_guidelines_manager = (
            character_guidelines_manager or CharacterGuidelinesManager()
        )
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def format(
        self,
    ) -> str:
        """Formats the character generation instructions with the loaded templates and place parameters."""
        playthrough_metadata = self._templates["playthrough_metadata"]
        character_generation_instructions = self._templates[
            "character_generation_instructions"
        ]

        world_name = playthrough_metadata["world_template"]
        region_name = self._places_templates_parameter.get_region_template()
        area_name = self._places_templates_parameter.get_area_template()
        location_name = self._places_templates_parameter.get_location_template()

        key = self._character_guidelines_manager.create_key(
            world_name, region_name, area_name, location_name
        )

        if not self._character_guidelines_manager.guidelines_exist(
            world_name, region_name, area_name, location_name
        ):
            raise ValueError(
                f"No character generation guidelines exist for key '{key}'."
            )

        formatted_instructions = character_generation_instructions.format(
            world_name=world_name,
            places_descriptions=self._places_descriptions,
            prohibited_names=self._characters_manager.get_all_character_names(),
            random_number=random.randint(-10, 10),
        )

        return formatted_instructions
