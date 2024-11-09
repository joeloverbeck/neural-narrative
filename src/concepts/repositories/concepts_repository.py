import logging
from typing import Optional, Dict, List

from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import read_json_file, write_json_file
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class ConceptsRepository:

    def __init__(
        self, playthrough_name: str, path_manager: Optional[PathManager] = None
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._path_manager = path_manager or PathManager()

        self._concepts_file_path = self._path_manager.get_concepts_file_path(
            playthrough_name
        )

    def _load_concepts_file(self) -> Dict[str, List[str]]:
        return read_json_file(self._concepts_file_path)

    def _has_concept(self, concept_key: str) -> bool:
        return concept_key in self._load_concepts_file()

    def add_concepts(self, concept_key: str, concepts: List[str]) -> None:
        concepts_file = self._load_concepts_file()

        if not self._has_concept(concept_key):
            concepts_file[concept_key] = []

        for concept in concepts:
            if not concept:
                raise ValueError(
                    f"Received a list with at least an invalid concept: {concepts}"
                )
            concepts_file[concept_key].append(concept)

        write_json_file(self._concepts_file_path, concepts_file)

        logger.info(f"Saved generated concepts to '{self._concepts_file_path}'.")
