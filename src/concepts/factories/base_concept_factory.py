from pathlib import Path
from typing import Optional

from src.concepts.algorithms.get_concepts_prompt_data_algorithm import (
    GetConceptsPromptDataAlgorithm,
)
from src.filesystem.path_manager import PathManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class BaseConceptFactory(BaseToolResponseProvider):

    def __init__(
        self,
        get_concepts_prompt_data_algorithm: GetConceptsPromptDataAlgorithm,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        prompt_file: Path,
        user_content: str,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        self._get_concepts_prompt_data_algorithm = get_concepts_prompt_data_algorithm
        self._prompt_file = prompt_file
        self._user_content = user_content

    def get_user_content(self) -> str:
        return self._user_content

    def get_prompt_file(self) -> Optional[Path]:
        return self._prompt_file

    def get_prompt_kwargs(self) -> dict:
        return self._get_concepts_prompt_data_algorithm.do_algorithm()
