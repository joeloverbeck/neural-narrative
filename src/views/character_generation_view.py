from flask import session, redirect, url_for, render_template, request
from flask.views import MethodView

from src.characters.characters_manager import CharactersManager
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
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
        characters_manager = CharactersManager(playthrough_name)
        guidelines = characters_manager.load_character_generation_guidelines(
            playthrough_manager.get_world_template(),
            places_templates_parameter.get_region_template(),
            places_templates_parameter.get_area_template(),
            places_templates_parameter.get_location_template(),
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
            return redirect(url_for("index"))

        action = request.form.get("action")
        if not action:
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

        CharacterService.generate_character(playthrough_name, guideline_text)

        # Optionally, add a success message to session
        session["character_generation_message"] = "Character generated successfully."

        # Clear the selected guideline
        session.pop("selected_guideline", None)

        return redirect(url_for("character-generation"))
