from flask import session, redirect, url_for, render_template, request
from flask.views import MethodView

from src.characters.characters_manager import CharactersManager
from src.enums import PlaceType
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.services.character_service import CharacterService
from src.services.place_service import PlaceService
from src.services.web_service import WebService
from src.time.time_manager import TimeManager


class LocationHubView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        current_place = MapManager(playthrough_name).get_current_place_template()
        characters_manager = CharactersManager(playthrough_name)
        characters_at_current_place = (
            characters_manager.get_characters_at_current_place()
        )
        WebService.format_image_urls_of_characters(characters_at_current_place)
        followers = characters_manager.get_followers()
        WebService.format_image_urls_of_characters(followers)
        map_manager = MapManager(playthrough_name)
        current_place_type = map_manager.get_current_place_type()
        locations_present = None

        if current_place_type == PlaceType.AREA:
            locations_present = map_manager.get_locations_in_area(
                PlaythroughManager(playthrough_name).get_current_place_identifier()
            )

        # Get current time
        time_manager = TimeManager(playthrough_name)
        current_hour = time_manager.get_hour()
        current_time_of_day = time_manager.get_time_of_the_day()

        return render_template(
            "location-hub.html",
            current_place=current_place,
            characters=characters_at_current_place,
            followers=followers,
            place_description=session.get("place_description", ""),
            current_place_type=current_place_type,
            locations_present=locations_present,
            current_hour=current_hour,
            current_time_of_day=current_time_of_day,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        action = request.form.get("action")
        if not action:
            return redirect(url_for("location-hub"))

        # Dispatch to the appropriate handler method
        method_name = f"handle_{action.replace(' ', '_').lower()}"
        method = getattr(self, method_name, None)

        if method:
            return method(playthrough_name)
        else:
            return redirect(url_for("location-hub"))

    @staticmethod
    def handle_add_to_followers(playthrough_name):
        selected_add = request.form.getlist("add_followers")
        CharacterService.add_followers(playthrough_name, selected_add)
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_remove_from_followers(playthrough_name):
        selected_remove = request.form.getlist("remove_followers")
        CharacterService.remove_followers(playthrough_name, selected_remove)
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_describe_place(playthrough_name):
        description = PlaceService.describe_place(playthrough_name)
        session["place_description"] = description
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_proceed_to_chat(playthrough_name):
        return redirect(url_for("participants"))

    @staticmethod
    def handle_exit_location(playthrough_name):
        PlaceService.exit_location(playthrough_name)
        session.pop("place_description", None)
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_visit_location(playthrough_name):
        location_identifier = request.form.get("location_identifier")
        PlaceService.visit_location(playthrough_name, location_identifier)
        session.pop("place_description", None)
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_advance_time(playthrough_name):
        TimeManager(playthrough_name).advance_time(5)
        return redirect(url_for("location-hub"))
