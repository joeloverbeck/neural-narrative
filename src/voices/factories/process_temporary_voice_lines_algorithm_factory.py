from pathlib import Path
from typing import List

from src.voices.algorithms.process_temporary_voice_lines_algorithm import (
    ProcessTemporaryVoiceLinesAlgorithm,
)


class ProcessTemporaryVoiceLinesAlgorithmFactory:
    def __init__(self, temp_file_paths: List[Path]):
        self._temp_file_paths = temp_file_paths

    def create_algorithm(self, file_name: Path) -> ProcessTemporaryVoiceLinesAlgorithm:
        return ProcessTemporaryVoiceLinesAlgorithm(self._temp_file_paths, file_name)
