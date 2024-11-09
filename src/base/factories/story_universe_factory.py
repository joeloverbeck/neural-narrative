from typing import Optional

from src.base.enums import TemplateType
from src.base.models.story_universe import StoryUniverse
from src.base.products.story_universe_product import StoryUniverseProduct
from src.filesystem.path_manager import PathManager
from src.maps.templates_repository import TemplatesRepository
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class StoryUniverseFactory(BaseToolResponseProvider):

    def __init__(
        self,
        story_universe_notion: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        path_manager: Optional[PathManager] = None,
        templates_repository: Optional[TemplatesRepository] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)
        self._story_universe_notion = story_universe_notion

        self._templates_repository = templates_repository or TemplatesRepository()

    def get_user_content(self) -> str:
        return f"Come up with a universe for a narrative based on the user's notion: {self._story_universe_notion}"

    def create_product_from_base_model(self, response_model: StoryUniverse):
        description = response_model.description

        return StoryUniverseProduct(
            response_model.name,
            description.replace("\n\n", "\n"),
            [category.lower() for category in response_model.categories],
        )

    def get_prompt_file(self) -> Optional[str]:
        return self._path_manager.get_story_universe_generation_prompt_path()

    def get_prompt_kwargs(self) -> dict:
        story_universes_file = self._templates_repository.load_templates(
            TemplateType.STORY_UNIVERSE
        )

        return {
            "story_universe_names": [key for key, value in story_universes_file.items()]
        }
