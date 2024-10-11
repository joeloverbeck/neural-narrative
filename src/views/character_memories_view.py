from flask import session, redirect, url_for, render_template, request
from flask.views import MethodView

from src.characters.algorithms.produce_self_reflection_algorithm import (
    ProduceSelfReflectionAlgorithm,
)
from src.characters.characters_manager import CharactersManager
from src.characters.factories.self_reflection_factory import SelfReflectionFactory
from src.config.config_manager import ConfigManager
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.services.web_service import WebService


class CharacterMemoriesView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        characters_manager = CharactersManager(playthrough_name)
        all_characters = characters_manager.get_all_characters()

        selected_character_identifier = request.args.get("character_identifier")
        character_memories = ""
        selected_character = None

        if selected_character_identifier:
            # Load the selected character's data
            selected_character = characters_manager.load_character_data(
                selected_character_identifier
            )
            # Load the character's memories
            character_memories = characters_manager.load_character_memories(
                selected_character_identifier
            )

        for character in all_characters:
            character["selected"] = False
            if (
                selected_character
                and character["identifier"] == selected_character["identifier"]
            ):
                character["selected"] = True

        self_reflection_text = session.pop("self_reflection_text", None)
        self_reflection_voice_line_url = session.pop(
            "self_reflection_voice_line_url", None
        )

        return render_template(
            "character-memories.html",
            all_characters=all_characters,
            selected_character=selected_character,
            character_memories=character_memories,
            self_reflection_text=self_reflection_text,
            self_reflection_voice_line_url=self_reflection_voice_line_url,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        characters_manager = CharactersManager(playthrough_name)

        action = request.form.get("action")
        character_identifier = request.form.get("character_identifier")

        if action == "save_memories" and character_identifier:
            new_memories = request.form.get("character_memories", "")

            # Normalize newlines to prevent issues with excessive newline characters
            new_memories = new_memories.replace("\r\n", "\n").strip()

            characters_manager.save_character_memories(
                character_identifier, new_memories
            )

            # Optionally, add a success message to the session
            session["memories_saved_message"] = "Memories saved successfully."
        elif action == "produce_self_reflection" and character_identifier:
            # Instantiate and execute the command
            produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
                OpenRouterLlmClientFactory().create_llm_client(),
                ConfigManager().get_heavy_llm(),
            )

            algorithm = ProduceSelfReflectionAlgorithm(
                playthrough_name,
                character_identifier,
                SelfReflectionFactory(
                    playthrough_name,
                    character_identifier,
                    produce_tool_response_strategy_factory,
                ),
            )

            # Execute the algorithm and get the result
            produce_self_reflection_product = algorithm.do_algorithm()

            # Extract the self-reflection text and voice line URL
            session["self_reflection_text"] = (
                produce_self_reflection_product.get_self_reflection()
            )
            session["self_reflection_voice_line_url"] = WebService.get_file_url(
                "voice_lines",
                produce_self_reflection_product.get_voice_line_file_name(),
            )

            # Add a success message
            session["memories_saved_message"] = (
                "Self-reflection produced and added to memories."
            )

        return redirect(
            url_for("character-memories", character_identifier=character_identifier)
        )
