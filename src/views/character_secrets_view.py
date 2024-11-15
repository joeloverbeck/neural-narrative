from flask import session, redirect, url_for, render_template, request, jsonify, flash
from flask.views import MethodView

from src.base.tools import capture_traceback
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.characters.commands.generate_character_secrets_command import (
    GenerateCharacterSecretsCommand,
)
from src.characters.configs.secrets_factory_config import SecretsFactoryConfig
from src.characters.configs.secrets_factory_factories_config import (
    SecretsFactoryFactoriesConfig,
)
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.retrieve_memories_algorithm_factory import (
    RetrieveMemoriesAlgorithmFactory,
)
from src.characters.factories.secrets_factory import SecretsFactory
from src.concepts.composers.format_known_facts_algorithm_composer import (
    FormatKnownFactsAlgorithmComposer,
)
from src.databases.chroma_db_database import ChromaDbDatabase
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
            try:
                produce_tool_response_strategy_factory = (
                    ProduceToolResponseStrategyFactoryComposer(
                        Llms().for_secrets_generation(),
                    ).compose_factory()
                )

                database = ChromaDbDatabase(playthrough_name)

                format_known_facts_algorithm = FormatKnownFactsAlgorithmComposer(
                    playthrough_name
                ).compose_algorithm()

                retrieve_memories_algorithm_factory = RetrieveMemoriesAlgorithmFactory(
                    database
                )

                character_factory = CharacterFactory(playthrough_name)

                secrets_factory = SecretsFactory(
                    SecretsFactoryConfig(playthrough_name, character_identifier),
                    format_known_facts_algorithm,
                    PlacesDescriptionsProviderComposer(
                        playthrough_name
                    ).compose_provider(),
                    SecretsFactoryFactoriesConfig(
                        produce_tool_response_strategy_factory,
                        retrieve_memories_algorithm_factory,
                        character_factory,
                    ),
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
