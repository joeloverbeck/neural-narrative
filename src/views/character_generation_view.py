import logging

from flask import session, redirect, url_for, render_template, request, jsonify, flash
from flask.views import MethodView

from src.base.exceptions import CharacterGenerationError
from src.base.playthrough_manager import PlaythroughManager
from src.base.tools import capture_traceback
from src.characters.algorithms.generate_character_generation_guidelines_algorithm import (
    GenerateCharacterGenerationGuidelinesAlgorithm,
)
from src.characters.character import Character
from src.characters.character_guidelines_manager import CharacterGuidelinesManager
from src.characters.characters_manager import CharactersManager
from src.characters.composers.character_generation_guidelines_provider_factory_composer import (
    CharacterGenerationGuidelinesProviderFactoryComposer,
)
from src.filesystem.file_operations import read_json_file
from src.filesystem.path_manager import PathManager
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.services.character_service import CharacterService
from src.services.web_service import WebService

logger = logging.getLogger(__name__)


class CharacterGenerationView(MethodView):

    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        playthrough_manager = PlaythroughManager(playthrough_name)
        places_templates_parameter = (
            HierarchyManagerFactory(playthrough_name)
            .create_hierarchy_manager()
            .fill_places_templates_parameter(
                playthrough_manager.get_current_place_identifier()
            )
        )
        character_guidelines_manager = CharacterGuidelinesManager()
        world_template = places_templates_parameter.get_world_template()
        region_template = places_templates_parameter.get_region_template()
        area_template = places_templates_parameter.get_area_template()
        location_template = places_templates_parameter.get_location_template()
        character_generation_guidelines = read_json_file(
            PathManager().get_character_generation_guidelines_path()
        )

        if (
            not character_guidelines_manager.create_key(
                playthrough_manager.get_story_universe_template(),
                world_template,
                region_template,
                area_template,
                location_template,
            )
            in character_generation_guidelines
        ):
            hierarchy_manager_factory = HierarchyManagerFactory(playthrough_name)
            GenerateCharacterGenerationGuidelinesAlgorithm(
                playthrough_name,
                playthrough_manager.get_current_place_identifier(),
                CharacterGenerationGuidelinesProviderFactoryComposer(
                    playthrough_name
                ).compose_factory(),
                hierarchy_manager_factory,
            ).do_algorithm()
        guidelines = character_guidelines_manager.load_guidelines(
            playthrough_manager.get_story_universe_template(),
            world_template,
            region_template,
            area_template,
            location_template,
        )
        character_generation_message = session.pop("character_generation_message", None)
        return render_template(
            "character-generation.html",
            guidelines=[guideline for guideline in guidelines],
            selected_guideline=session.get("selected_guideline", ""),
            character_generation_message=character_generation_message,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": "Session expired."}), 400
            else:
                return redirect(url_for("index"))
        action = request.form.get("submit_action")
        if not action:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": "Invalid action."}), 400
            else:
                return redirect(url_for("character-generation"))
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
            response = {
                "success": True,
                "message": f"Character '{Character(playthrough_name, latest_identifier).name}' generated successfully.",
            }
        except CharacterGenerationError as e:
            logger.error("Failed to generate character. Error: %s", e)
            response = {
                "success": False,
                "error": f"Character generation failed. Error: {str(e)}",
            }
        except Exception as e:
            capture_traceback()
            logger.error("Unspecified error. Error: %s", e)
            response = {"success": False, "error": f"Unspecified error: {str(e)}"}
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify(response)
        else:
            session["character_generation_message"] = response.get(
                "message"
            ) or response.get("error")
            return redirect(url_for("character-generation"))

    @staticmethod
    def handle_generate_guidelines(playthrough_name):
        try:
            playthrough_manager = PlaythroughManager(playthrough_name)
            place_identifier = playthrough_manager.get_current_place_identifier()
            hierarchy_manager_factory = HierarchyManagerFactory(playthrough_name)
            product = GenerateCharacterGenerationGuidelinesAlgorithm(
                playthrough_name,
                place_identifier,
                CharacterGenerationGuidelinesProviderFactoryComposer(
                    playthrough_name
                ).compose_factory(),
                hierarchy_manager_factory,
            ).do_algorithm()
            if not product.is_valid():
                raise ValueError(
                    "Failed to generate guidelines: " + product.get_error()
                )
            guidelines = product.get()
            response = {
                "success": True,
                "message": "Guidelines generated successfully.",
                "guidelines": [guideline for guideline in guidelines],
            }
        except Exception as e:
            capture_traceback()
            logger.error("Failed to generate guidelines. Error: %s", e)
            response = {
                "success": False,
                "error": f"Failed to generate guidelines. Error: {str(e)}",
            }
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify(response)
        else:
            flash("Guidelines generated successfully.")
            return redirect(url_for("chat"))
