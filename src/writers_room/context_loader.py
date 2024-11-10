from typing import Optional, Dict

from src.concepts.enums import ConceptType
from src.concepts.repositories.facts_repository import FactsRepository
from src.filesystem.file_operations import read_file, read_json_file
from src.filesystem.path_manager import PathManager
from src.maps.composers.places_descriptions_provider_composer import (
    PlacesDescriptionsProviderComposer,
)


class ContextLoader:
    def __init__(
        self,
        playthrough_name,
        path_manager: Optional[PathManager] = None,
        facts_repository: Optional[FactsRepository] = None,
    ):
        self._playthrough_name = playthrough_name

        self._path_manager = path_manager or PathManager()
        self._facts_repository = facts_repository or FactsRepository(playthrough_name)

    def load_context_variables(self) -> Dict[str, str]:
        context_file = read_file(
            self._path_manager.get_writers_room_context_path(self._playthrough_name)
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

        # Note that if any of such concepts hasn't been generated, this would fail unless handled.
        plot_blueprints = (
            concepts_file[ConceptType.PLOT_BLUEPRINTS.value]
            if ConceptType.PLOT_BLUEPRINTS.value in concepts_file
            else ""
        )
        goals = (
            concepts_file[ConceptType.GOALS.value]
            if ConceptType.GOALS.value in concepts_file
            else ""
        )
        plot_twists = (
            concepts_file[ConceptType.PLOT_TWISTS.value]
            if ConceptType.PLOT_TWISTS.value in concepts_file
            else ""
        )
        scenarios = (
            concepts_file[ConceptType.SCENARIOS.value]
            if ConceptType.SCENARIOS.value in concepts_file
            else ""
        )
        dilemmas = (
            concepts_file[ConceptType.DILEMMAS.value]
            if ConceptType.DILEMMAS.value in concepts_file
            else ""
        )

        context_variables = {
            "context": context_file,
            "facts": self._facts_repository.load_facts_file(),
            "characters": characters_file,
            "places_descriptions": places_descriptions,
            ConceptType.PLOT_BLUEPRINTS.value: plot_blueprints,
            ConceptType.GOALS.value: goals,
            ConceptType.PLOT_TWISTS.value: plot_twists,
            ConceptType.SCENARIOS.value: scenarios,
            ConceptType.DILEMMAS.value: dilemmas,
        }

        return context_variables
