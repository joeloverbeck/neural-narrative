from typing import Optional

from src.base.constants import (
    STORY_UNIVERSE_GENERATION_PROMPT_FILE,
    STORY_UNIVERSE_GENERATION_TOOL_FILE,
    STORY_UNIVERSES_TEMPLATE_FILE,
)
from src.base.products.story_universe_product import StoryUniverseProduct
from src.base.required_string import RequiredString
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class StoryUniverseFactory(BaseToolResponseProvider):
    def __init__(
        self,
        story_universe_notion: RequiredString,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._story_universe_notion = story_universe_notion

    def get_tool_file(self) -> str:
        return STORY_UNIVERSE_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return f"Come up with a universe for a narrative based on the user's notion: {self._story_universe_notion.value}"

    def create_product(self, arguments: dict):
        return StoryUniverseProduct(
            RequiredString(arguments.get("name")),
            RequiredString(arguments.get("description")),
            [
                RequiredString(arguments.get("category_1")),
                RequiredString(arguments.get("category_2")),
            ],
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
