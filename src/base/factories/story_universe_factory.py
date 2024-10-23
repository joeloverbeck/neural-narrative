from typing import Optional

from src.base.constants import (
    STORY_UNIVERSE_GENERATION_PROMPT_FILE,
    STORY_UNIVERSES_TEMPLATE_FILE,
)
from src.base.models.story_universe import StoryUniverse
from src.base.products.story_universe_product import StoryUniverseProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class StoryUniverseFactory(BaseToolResponseProvider):

    def __init__(
        self,
        story_universe_notion: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)
        self._story_universe_notion = story_universe_notion

    def _get_tool_data(self) -> dict:
        return StoryUniverse.model_json_schema()

    def get_user_content(self) -> str:
        return f"Come up with a universe for a narrative based on the user's notion: {self._story_universe_notion}"

    def create_product_from_base_model(self, base_model: StoryUniverse):
        return StoryUniverseProduct(
            base_model.name, base_model.description, base_model.categories
        )

    def get_prompt_file(self) -> Optional[str]:
        return STORY_UNIVERSE_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        story_universes_file = self._filesystem_manager.load_existing_or_new_json_file(
            STORY_UNIVERSES_TEMPLATE_FILE
        )
        return {
            "story_universe_names": [key for key, value in story_universes_file.items()]
        }
