from flask import session, redirect, url_for, render_template, request
from flask.views import MethodView

from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.characters.commands.generate_character_secrets_command import (
    GenerateCharacterSecretsCommand,
)
from src.characters.factories.secrets_factory import SecretsFactory
from src.config.config_manager import ConfigManager
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class CharacterSecretsView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        characters_manager = CharactersManager(playthrough_name)
        all_characters = characters_manager.get_all_characters()

        selected_character_identifier = request.args.get("character_identifier")
        selected_character = None

        # Retrieve any success or error messages from the session
        secrets_generated_message = session.pop("secrets_generated_message", None)

        if selected_character_identifier:
            # Load the selected character's data
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

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        action = request.form.get("action")
        character_identifier = request.form.get("character_identifier")

        if action == "generate_secrets" and character_identifier:
            try:
                produce_tool_response_strategy_factory = (
                    ProduceToolResponseStrategyFactory(
                        OpenRouterLlmClientFactory().create_llm_client(),
                        ConfigManager().get_heavy_llm(),
                    )
                )
                place_descriptions_factory = PlaceDescriptionsForPromptFactory(
                    playthrough_name
                )

                places_descriptions_factory = PlacesDescriptionsFactory(
                    place_descriptions_factory
                )

                secrets_factory = SecretsFactory(
                    playthrough_name,
                    character_identifier,
                    produce_tool_response_strategy_factory,
                    places_descriptions_factory,
                )
                command = GenerateCharacterSecretsCommand(
                    playthrough_name, character_identifier, secrets_factory
                )
                # Execute the command to generate secrets
                try:
                    command.execute()
                    # Set a success message
                    session["secrets_generated_message"] = (
                        "Secrets generated successfully."
                    )
                except Exception as exception:
                    # Set a success message
                    session["secrets_generated_message"] = (
                        f"Failed to generate secrets. Error: {exception}"
                    )

            except Exception as e:
                # Handle any errors and set an error message
                session["secrets_generated_message"] = f"An error occurred: {str(e)}"

            # Redirect back to the secrets page with the selected character
            return redirect(
                url_for("character-secrets", character_identifier=character_identifier)
            )
        else:
            # If no action is specified or character_identifier is missing, redirect back
            return redirect(url_for("character-secrets"))
