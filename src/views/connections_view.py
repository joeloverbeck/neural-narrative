from flask import session, redirect, url_for, render_template, request, jsonify
from flask.views import MethodView

from src.characters.characters_manager import CharactersManager
from src.characters.commands.generate_connection_command import (
    GenerateConnectionCommand,
)
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.character_information_provider_factory import (
    CharacterInformationProviderFactory,
)
from src.characters.factories.connection_factory import ConnectionFactory
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.characters.models.connection import Connection
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.enums import LlmClientType
from src.prompting.llms import Llms


class ConnectionsView(MethodView):

    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        characters_manager = CharactersManager(playthrough_name)
        all_characters = characters_manager.get_all_characters()
        return render_template("connections.html", all_characters=all_characters)

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return jsonify({"success": False, "error": "Playthrough name not found."})
        action = request.form.get("submit_action")
        if action != "generate_connection":
            return jsonify({"success": False, "error": "Invalid action."})
        character_a_identifier = request.form.get("character_a_identifier", "").strip()
        character_b_identifier = request.form.get("character_b_identifier", "").strip()
        if not character_a_identifier or not character_b_identifier:
            return jsonify(
                {"success": False, "error": "Both characters must be selected."}
            )
        if character_a_identifier == character_b_identifier:
            return jsonify(
                {"success": False, "error": "Please select two different characters."}
            )
        try:

            produce_tool_response_strategy_factory = (
                ProduceToolResponseStrategyFactoryComposer(
                    LlmClientType.INSTRUCTOR,
                    Llms().for_character_connection(),
                    Connection,
                ).compose_factory()
            )
            character_information_provider_factory = (
                CharacterInformationProviderFactory(playthrough_name)
            )

            character_factory = CharacterFactory(playthrough_name)

            connection_factory = ConnectionFactory(
                character_a_identifier,
                character_b_identifier,
                character_factory,
                character_information_provider_factory,
                produce_tool_response_strategy_factory,
            )
            store_character_memory_command_factory = StoreCharacterMemoryCommandFactory(
                playthrough_name
            )
            command = GenerateConnectionCommand(
                character_a_identifier,
                character_b_identifier,
                connection_factory,
                store_character_memory_command_factory,
            )
            command.execute()
            return jsonify(
                {"success": True, "message": "Connection generated successfully."}
            )
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
