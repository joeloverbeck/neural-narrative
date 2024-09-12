from src.constants import WORLD_GENERATION_PROMPT_FILE, WORLD_GENERATION_TOOL_FILE, TOOL_INSTRUCTIONS_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.strategies import PlaceGenerationStrategy
from src.prompting.abstracts.strategies import ProduceToolResponseStrategy
from src.prompting.prompting import prompt_for_input
from src.tools import generate_tool_prompt


class WorldGenerationStrategy(PlaceGenerationStrategy):
    def __init__(self, produce_tool_response_strategy: ProduceToolResponseStrategy):
        assert produce_tool_response_strategy

        self._produce_tool_response_strategy = produce_tool_response_strategy

    def generate_place(self):
        world_notion = prompt_for_input("What are your notions about how this world should be like?: ")

        filesystem_manager = FilesystemManager()

        world_names = list(filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_worlds_template_file()).keys())

        world_generation_prompt = filesystem_manager.read_file(WORLD_GENERATION_PROMPT_FILE).format(
            world_names=world_names
        )

        system_content = world_generation_prompt + "\n\n" + generate_tool_prompt(
            filesystem_manager.read_json_file(WORLD_GENERATION_TOOL_FILE),
            filesystem_manager.read_file(TOOL_INSTRUCTIONS_FILE))

        user_content = ("Create the name, description, and two fitting categories for a world, following the "
                        "above instructions as well as the following notions provided by the user about "
                        f"how they want the world to be: {world_notion}")

        tool_response = self._produce_tool_response_strategy.produce_tool_response(system_content,
                                                                                   user_content)

        print(tool_response)

        # Extract the "arguments" dictionary from the tool response
        arguments = tool_response.get("arguments", {})

        # Build the result JSON from the extracted fields
        world_data = {
            "name": arguments.get("name"),
            "description": arguments.get("description"),
            "categories": arguments.get("categories")
        }

        worlds_template_file = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_worlds_template_file())

        worlds_template_file.update({
            world_data["name"]: {
                "description": world_data["description"],
                "categories": world_data["categories"]
            }
        })

        filesystem_manager.save_json_file(worlds_template_file,
                                          filesystem_manager.get_file_path_to_worlds_template_file())

        print(f"Saved world template '{world_data["name"]}'.")
