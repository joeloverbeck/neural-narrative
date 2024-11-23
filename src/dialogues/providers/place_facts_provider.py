import logging
from pathlib import Path
from typing import Optional

from openai import BaseModel

from src.base.products.dict_product import DictProduct
from src.base.validators import validate_non_empty_string
from src.filesystem.path_manager import PathManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider

logger = logging.getLogger(__name__)


class PlaceFactsProvider(BaseToolResponseProvider):
    def __init__(
        self,
        place_description: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        validate_non_empty_string(place_description, "place_description")

        self._place_description = place_description

    def get_prompt_file(self) -> Path:
        return self._path_manager.get_place_facts_generation_prompt()

    def get_user_content(self) -> str:
        return "Succintly summarize the facts about the place based on the description above -- think short, concise bullet points."

    def create_product_from_base_model(self, response_model: BaseModel):
        # Log chain of thought.
        logger.info(
            "Place facts reasoning: %s",
            response_model.place_facts.chain_of_thought,
        )

        return DictProduct(response_model.place_facts.place_facts, is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        return {
            "place_description": self._place_description,
        }
