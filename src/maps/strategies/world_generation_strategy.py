import logging

from src.constants import (
    WORLD_GENERATION_PROMPT_FILE,
    WORLD_GENERATION_TOOL_FILE,
    TOOL_INSTRUCTIONS_FILE,
)
from src.enums import TemplateType
from src.filesystem.filesystem_manager import FilesystemManager
from src.interfaces.abstracts.interface_manager import InterfaceManager
from src.interfaces.console_interface_manager import ConsoleInterfaceManager
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
            produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
            interface_manager: InterfaceManager = None,
            filesystem_manager: FilesystemManager = None,
    ):
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

        self._interface_manager = interface_manager or ConsoleInterfaceManager()
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def generate_place(self):
        world_notion = self._interface_manager.prompt_for_input(
            "What are your notions about how this world should be like?: "
        )

        world_names = list(
            self._filesystem_manager.load_existing_or_new_json_file(
                self._filesystem_manager.get_file_path_to_worlds_template_file()
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
            f"how they want the world to be: {world_notion}"
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

        StoreGeneratedPlaceCommand(world_data, TemplateType.WORLD)
