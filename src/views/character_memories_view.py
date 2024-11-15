import logging

from flask import session, redirect, url_for, render_template, request, jsonify
from flask.views import MethodView

from src.base.tools import capture_traceback
from src.characters.algorithms.produce_self_reflection_algorithm import (
    ProduceSelfReflectionAlgorithm,
)
from src.characters.algorithms.produce_worldview_algorithm import (
    ProduceWorldviewAlgorithm,
)
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.characters.composers.character_information_provider_factory_composer import (
    CharacterInformationProviderFactoryComposer,
)
from src.characters.factories.self_reflection_factory import SelfReflectionFactory
from src.characters.factories.worldview_factory import WorldviewFactory
from src.databases.chroma_db_database import ChromaDbDatabase
from src.interfaces.web_interface_manager import WebInterfaceManager
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms

logger = logging.getLogger(__name__)


class CharacterMemoriesView(MethodView):

    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        characters_manager = CharactersManager(playthrough_name)
        all_characters = characters_manager.get_all_characters()
        selected_character_identifier = request.args.get("character_identifier")
        selected_character = None

        if selected_character_identifier:
            selected_character = Character(
                playthrough_name, selected_character_identifier
            )

        for character in all_characters:
            character["selected"] = False
            if (
                selected_character
                and character["identifier"] == selected_character.identifier
            ):
                character["selected"] = True

        self_reflection_text = session.pop("self_reflection_text", None)
        worldview_text = session.pop("worldview_text", None)

        return render_template(
            "character-memories.html",
            all_characters=all_characters,
            selected_character=selected_character,
            self_reflection_text=self_reflection_text,
            worldview_text=worldview_text,
        )

    @staticmethod
    def post():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        action = request.form.get("submit_action")
        character_identifier = request.form.get("character_identifier")
        if action == "insert_memory" and character_identifier:
            new_memory = request.form.get("character_memory", "")
            new_memory = WebInterfaceManager.remove_excessive_newline_characters(
                new_memory
            )

            new_memories = new_memory.splitlines()

            if not new_memories:
                response = {
                    "success": False,
                    "error": "No memory to save.",
                }
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(response)
                else:
                    return redirect(url_for("story-hub"))
            try:
                database = ChromaDbDatabase(playthrough_name)

                logger.info("Memories to add: %s", new_memories)

                [
                    database.insert_memory(character_identifier, memory)
                    for memory in new_memories
                    if memory
                ]

                response = {
                    "success": True,
                    "message": "Memory saved.",
                }
            except Exception as e:
                capture_traceback()
                response = {
                    "success": False,
                    "error": f"Unable to save memory. Error: {str(e)}",
                }

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
            else:
                return redirect(url_for("character-memories"))
        elif action == "query_memories" and character_identifier:
            query_text = request.form.get("query", "")
            top_k = request.form.get("top_k", 5)

            try:
                top_k = int(top_k)
            except ValueError:
                top_k = 5

            if not query_text.strip():
                response = {
                    "success": False,
                    "error": "Please enter a query.",
                }
                return jsonify(response)

            try:
                database = ChromaDbDatabase(playthrough_name)
                memories = database.retrieve_memories(
                    character_identifier, query_text, top_k=top_k
                )
                response = {
                    "success": True,
                    "message": "Query successful.",
                    "results": memories,
                }
            except Exception as e:
                capture_traceback()
                response = {
                    "success": False,
                    "error": f"Unable to retrieve memories. Error: {str(e)}",
                }

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
            else:
                return redirect(url_for("character-memories"))
        elif action == "produce_worldview" and character_identifier:
            subject = request.form.get("worldview_subject")

            produce_tool_response_strategy_factory = (
                ProduceToolResponseStrategyFactoryComposer(
                    Llms().for_worldview(),
                ).compose_factory()
            )

            character_information_factory = CharacterInformationProviderFactoryComposer(
                playthrough_name
            ).compose_factory(character_identifier)

            worldview_factory = WorldviewFactory(
                playthrough_name,
                character_identifier,
                subject,
                produce_tool_response_strategy_factory,
                character_information_factory,
            )

            algorithm = ProduceWorldviewAlgorithm(
                playthrough_name, character_identifier, worldview_factory
            )

            product = algorithm.do_algorithm()

            session["worldview_text"] = product.get()

            response = {
                "success": True,
                "message": "Worldview produced.",
                "worldview_text": product.get(),
            }

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
            else:
                return redirect(url_for("character-memories"))
        elif action == "produce_self_reflection" and character_identifier:
            subject = request.form.get("self_reflection_subject")

            if not subject:
                response = {
                    "success": False,
                    "error": "You must provide the subject to self-reflect about.",
                }

                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(response)
                else:
                    return redirect(url_for("character-memories"))

            produce_tool_response_strategy_factory = (
                ProduceToolResponseStrategyFactoryComposer(
                    Llms().for_self_reflection(),
                ).compose_factory()
            )

            character_information_provider_factory = (
                CharacterInformationProviderFactoryComposer(
                    playthrough_name
                ).compose_factory(character_identifier)
            )

            algorithm = ProduceSelfReflectionAlgorithm(
                playthrough_name,
                Character(playthrough_name, character_identifier),
                SelfReflectionFactory(
                    playthrough_name,
                    character_identifier,
                    subject,
                    produce_tool_response_strategy_factory,
                    character_information_provider_factory,
                ),
            )

            produce_self_reflection_product = algorithm.do_algorithm()
            session["self_reflection_text"] = produce_self_reflection_product.get()

            response = {
                "success": True,
                "message": "Self-reflection produced.",
                "self_reflection_text": produce_self_reflection_product.get(),
            }

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
            else:
                return redirect(url_for("character-memories"))
        return redirect(
            url_for("character-memories", character_identifier=character_identifier)
        )
