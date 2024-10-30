from flask import session, redirect, url_for, render_template, request, jsonify, flash
from flask.views import MethodView

from src.base.tools import capture_traceback
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.characters.commands.generate_character_secrets_command import (
    GenerateCharacterSecretsCommand,
)
from src.characters.factories.secrets_factory import SecretsFactory
from src.maps.composers.places_descriptions_provider_composer import (
    PlacesDescriptionsProviderComposer,
)
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms


class CharacterSecretsView(MethodView):

    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        characters_manager = CharactersManager(playthrough_name)
        all_characters = characters_manager.get_all_characters()
        selected_character_identifier = request.args.get("character_identifier")
        selected_character = None
        secrets_generated_message = session.pop("secrets_generated_message", None)
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
        return render_template(
            "character-secrets.html",
            all_characters=all_characters,
            selected_character=selected_character,
            secrets_generated_message=secrets_generated_message,
        )

    @staticmethod
    def post():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        action = request.form.get("submit_action")
        character_identifier = request.form.get("character_identifier")
        if action == "generate_secrets" and character_identifier:
            response = {}
            try:
                produce_tool_response_strategy_factory = (
                    ProduceToolResponseStrategyFactoryComposer(
                        Llms().for_secrets_generation(),
                    ).compose_factory()
                )
                secrets_factory = SecretsFactory(
                    playthrough_name,
                    character_identifier,
                    produce_tool_response_strategy_factory,
                    PlacesDescriptionsProviderComposer(
                        playthrough_name
                    ).compose_provider(),
                )
                command = GenerateCharacterSecretsCommand(
                    playthrough_name, character_identifier, secrets_factory
                )
                try:
                    command.execute()
                    session["secrets_generated_message"] = (
                        "Secrets generated successfully."
                    )

                    response = {
                        "success": True,
                        "message": "Secret generated and added to character bio.",
                    }
                except Exception as exception:
                    session["secrets_generated_message"] = (
                        f"Failed to generate secrets. Error: {exception}"
                    )
                    raise
            except Exception as e:
                capture_traceback()

                error_message = f"Failed to create secret. Error: {str(e)}."
                response = {
                    "success": False,
                    "error": error_message,
                }
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(response)
                else:
                    flash(error_message, "error")
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
        else:
            return redirect(url_for("character-secrets"))
