from flask import session, redirect, url_for, render_template, request
from flask.views import MethodView

from src.characters.algorithms.produce_self_reflection_algorithm import (
    ProduceSelfReflectionAlgorithm,
)
from src.characters.character import Character
from src.characters.character_memories import CharacterMemories
from src.characters.characters_manager import CharactersManager
from src.characters.factories.character_information_provider import (
    CharacterInformationProvider,
)
from src.characters.factories.self_reflection_factory import SelfReflectionFactory
from src.interfaces.web_interface_manager import WebInterfaceManager
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms
from src.services.web_service import WebService
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)


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
            selected_character = Character(
                playthrough_name, selected_character_identifier
            )
            character_memories = CharacterMemories(playthrough_name).load_memories(
                selected_character
            )
        for character in all_characters:
            character["selected"] = False
            if (
                selected_character
                and character["identifier"] == selected_character.identifier
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
        action = request.form.get("action")
        character_identifier = request.form.get("character_identifier")
        if action == "save_memories" and character_identifier:
            new_memories = request.form.get("character_memories", "")
            new_memories = WebInterfaceManager.remove_excessive_newline_characters(
                new_memories
            )
            CharacterMemories(playthrough_name).save_memories(
                Character(playthrough_name, character_identifier), new_memories
            )
            session["memories_saved_message"] = "Memories saved successfully."
        elif action == "produce_self_reflection" and character_identifier:
            produce_tool_response_strategy_factory = (
                ProduceToolResponseStrategyFactoryComposer(
                    Llms().for_self_reflection(),
                ).compose_factory()
            )
            character_information_factory = CharacterInformationProvider(
                playthrough_name, character_identifier
            )
            algorithm = ProduceSelfReflectionAlgorithm(
                playthrough_name,
                character_identifier,
                SelfReflectionFactory(
                    playthrough_name,
                    character_identifier,
                    produce_tool_response_strategy_factory,
                    character_information_factory,
                ),
                DirectVoiceLineGenerationAlgorithmFactory(),
            )
            produce_self_reflection_product = algorithm.do_algorithm()
            session["self_reflection_text"] = (
                produce_self_reflection_product.get_self_reflection()
            )
            session["self_reflection_voice_line_url"] = WebService.get_file_url(
                "voice_lines",
                produce_self_reflection_product.get_voice_line_file_name(),
            )
            session["memories_saved_message"] = (
                "Self-reflection produced and added to memories."
            )
        return redirect(
            url_for("character-memories", character_identifier=character_identifier)
        )
