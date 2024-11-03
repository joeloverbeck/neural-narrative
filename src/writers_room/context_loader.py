from typing import Optional, Dict

from src.concepts.enums import ConceptType
from src.filesystem.file_operations import read_file, read_json_file
from src.filesystem.path_manager import PathManager
from src.maps.composers.places_descriptions_provider_composer import (
    PlacesDescriptionsProviderComposer,
)


class ContextLoader:
    def __init__(self, playthrough_name, path_manager: Optional[PathManager] = None):
        self._playthrough_name = playthrough_name

        self._path_manager = path_manager or PathManager()

    def load_context_variables(self) -> Dict[str, str]:
        context_file = read_file(
            self._path_manager.get_writers_room_context_path(self._playthrough_name)
        )
        facts_file = read_file(
            self._path_manager.get_facts_path(self._playthrough_name)
        )
        characters_file = read_json_file(
            self._path_manager.get_characters_file_path(self._playthrough_name)
        )

        places_descriptions = (
            PlacesDescriptionsProviderComposer(self._playthrough_name)
            .compose_provider()
            .get_information()
        )

        concepts_file = read_json_file(
            self._path_manager.get_concepts_file_path(self._playthrough_name)
        )

        context_variables = {
            "context": context_file,
            "facts": facts_file,
            "characters": characters_file,
            "places_descriptions": places_descriptions,
            ConceptType.PLOT_BLUEPRINTS.value: concepts_file[
                ConceptType.PLOT_BLUEPRINTS.value
            ],
            ConceptType.GOALS.value: concepts_file[ConceptType.GOALS.value],
            ConceptType.PLOT_TWISTS.value: concepts_file[ConceptType.PLOT_TWISTS.value],
            ConceptType.SCENARIOS.value: concepts_file[ConceptType.SCENARIOS.value],
            ConceptType.DILEMMAS.value: concepts_file[ConceptType.DILEMMAS.value],
        }

        return context_variables
