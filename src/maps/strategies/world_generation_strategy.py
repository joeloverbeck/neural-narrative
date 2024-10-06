import logging

from src.constants import (
    WORLD_GENERATION_PROMPT_FILE,
    WORLD_GENERATION_TOOL_FILE,
    TOOL_INSTRUCTIONS_FILE,
    WORLD_TEMPLATES_FILE,
)
from src.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.strategies import PlaceGenerationStrategy
from src.maps.commands.store_generated_place_command import StoreGeneratedPlaceCommand
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.tools import generate_tool_prompt

logger = logging.getLogger(__name__)


class WorldGenerationStrategy(PlaceGenerationStrategy):
    def __init__(
        self,
        world_notion: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: FilesystemManager = None,
    ):
        if not world_notion:
            raise ValueError("world_notion can't be empty.")

        self._world_notion = world_notion
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def generate_place(self):
        world_names = list(
            self._filesystem_manager.load_existing_or_new_json_file(
                WORLD_TEMPLATES_FILE
            ).keys()
        )

        world_generation_prompt = self._filesystem_manager.read_file(
            WORLD_GENERATION_PROMPT_FILE
        ).format(world_names=world_names)

        system_content = (
            world_generation_prompt
            + "\n\n"
            + generate_tool_prompt(
                self._filesystem_manager.read_json_file(WORLD_GENERATION_TOOL_FILE),
                self._filesystem_manager.read_file(TOOL_INSTRUCTIONS_FILE),
            )
        )

        user_content = (
            "Create the name, description, and two fitting categories for a world, following the "
            "above instructions as well as the following notions provided by the user about "
            f"how they want the world to be: {self._world_notion}"
        )

        tool_response = self._produce_tool_response_strategy_factory.create_produce_tool_response_strategy().produce_tool_response(
            system_content, user_content
        )

        # Extract the "arguments" dictionary from the tool response
        arguments = tool_response.get("arguments", {})

        # Build the result JSON from the extracted fields
        world_data = {
            "name": arguments.get("name"),
            "description": arguments.get("description"),
            "categories": arguments.get("categories"),
        }

        logger.info(f"World produced:\n{world_data}")

        # Optionally store the generated world
        StoreGeneratedPlaceCommand(world_data, TemplateType.WORLD).execute()
