from flask import session, redirect, url_for, render_template, request, jsonify, flash
from flask.views import MethodView

from src.characters.algorithms.generate_character_generation_guidelines_algorithm import (
    GenerateCharacterGenerationGuidelinesAlgorithm,
)
from src.characters.character import Character
from src.characters.character_guidelines_manager import CharacterGuidelinesManager
from src.characters.characters_manager import CharactersManager
from src.characters.factories.character_generation_guidelines_factory import (
    CharacterGenerationGuidelinesFactory,
)
from src.config.config_manager import ConfigManager
from src.constants import CHARACTER_GENERATION_GUIDELINES_FILE
from src.exceptions import CharacterGenerationFailedError
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.services.character_service import CharacterService
from src.services.web_service import WebService


class CharacterGenerationView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        # Get current place's details
        playthrough_manager = PlaythroughManager(playthrough_name)
        map_manager = MapManager(playthrough_name)

        places_templates_parameter = map_manager.fill_places_templates_parameter(
            playthrough_manager.get_current_place_identifier()
        )

        # Load the guidelines
        character_guidelines_manager = CharacterGuidelinesManager()

        world_template = playthrough_manager.get_world_template()
        region_template = places_templates_parameter.get_region_template()
        area_template = places_templates_parameter.get_area_template()
        location_template = places_templates_parameter.get_location_template()

        filesystem_manager = FilesystemManager()

        character_generation_guidelines = (
            filesystem_manager.load_existing_or_new_json_file(
                CHARACTER_GENERATION_GUIDELINES_FILE
            )
        )

        # First ensure that the guidelines exist.
        if (
            not character_guidelines_manager.create_key(
                world_template, region_template, area_template, location_template
            )
            in character_generation_guidelines
        ):
            place_descriptions_for_prompt_factory = PlaceDescriptionsForPromptFactory(
                playthrough_name
            )

            places_descriptions_factory = PlacesDescriptionsFactory(
                place_descriptions_for_prompt_factory
            )

            # Need to create the guidelines.
            character_generation_guidelines_factory = (
                CharacterGenerationGuidelinesFactory(
                    playthrough_name,
                    playthrough_manager.get_current_place_identifier(),
                    ProduceToolResponseStrategyFactory(
                        OpenRouterLlmClientFactory().create_llm_client(),
                        ConfigManager().get_heavy_llm(),
                    ),
                    places_descriptions_factory,
                )
            )

            GenerateCharacterGenerationGuidelinesAlgorithm(
                playthrough_name,
                playthrough_manager.get_current_place_identifier(),
                character_generation_guidelines_factory,
            ).do_algorithm()

        guidelines = character_guidelines_manager.load_guidelines(
            world_template,
            region_template,
            area_template,
            location_template,
        )

        # Get any messages
        character_generation_message = session.pop("character_generation_message", None)

        return render_template(
            "character-generation.html",
            guidelines=guidelines,
            selected_guideline=session.get("selected_guideline", ""),
            character_generation_message=character_generation_message,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Session expired.",
                        }
                    ),
                    400,
                )
            else:
                return redirect(url_for("index"))

        action = request.form.get("submit_action")
        if not action:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": "Invalid action."}), 400
            else:
                return redirect(url_for("character-generation"))

        # Dispatch to the appropriate handler method
        method_name = WebService.create_method_name(action)
        method = getattr(self, method_name, None)

        if method:
            return method(playthrough_name)
        else:
            return redirect(url_for("character-generation"))

    @staticmethod
    def handle_generate_character(playthrough_name):
        guideline_text = request.form.get("guideline_text")

        try:
            CharacterService.generate_character(playthrough_name, guideline_text)

            latest_identifier = CharactersManager(
                playthrough_name
            ).get_latest_character_identifier()

            # Prepare the response
            response = {
                "success": True,
                "message": f"Character '{Character(playthrough_name, latest_identifier).name}' generated successfully.",
            }
        except CharacterGenerationFailedError as e:
            response = {
                "success": False,
                "error": f"Character generation failed. Error: {str(e)}",
            }
        except Exception as e:
            response = {"success": False, "error": f"Unspecific error: {str(e)}"}

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify(response)
        else:
            # For non-AJAX requests, handle as before
            session["character_generation_message"] = response.get(
                "message"
            ) or response.get("error")
            return redirect(url_for("character-generation"))

    @staticmethod
    def handle_generate_guidelines(playthrough_name):
        try:
            playthrough_manager = PlaythroughManager(playthrough_name)

            place_identifier = playthrough_manager.get_current_place_identifier()

            produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
                OpenRouterLlmClientFactory().create_llm_client(),
                ConfigManager().get_heavy_llm(),
            )

            place_descriptions_for_prompt_factory = PlaceDescriptionsForPromptFactory(
                playthrough_name
            )

            places_descriptions_factory = PlacesDescriptionsFactory(
                place_descriptions_for_prompt_factory
            )

            character_generation_guidelines_factory = (
                CharacterGenerationGuidelinesFactory(
                    playthrough_name,
                    place_identifier,
                    produce_tool_response_strategy_factory,
                    places_descriptions_factory,
                )
            )

            # Product could be used to return it to the page and show the guidelines
            # without having to refresh the page.
            product = GenerateCharacterGenerationGuidelinesAlgorithm(
                playthrough_name,
                place_identifier,
                character_generation_guidelines_factory,
            ).do_algorithm()

            # Ensure the product is valid
            if not product.is_valid():
                raise ValueError(
                    "Failed to generate guidelines: " + product.get_error()
                )

            # Get the generated guidelines
            guidelines = product.get()

            response = {
                "success": True,
                "message": "Guidelines generated successfully.",
                "guidelines": guidelines,  # Include the guidelines in the response
            }
        except Exception as e:
            response = {
                "success": False,
                "error": f"Failed to generate guidelines. Error: {str(e)}",
            }

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify(response)
        else:
            flash("Guidelines generated successfully.")
            return redirect(url_for("chat"))
