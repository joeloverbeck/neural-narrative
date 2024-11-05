import logging
from pathlib import Path

from flask import (
    session,
    redirect,
    url_for,
    render_template,
    request,
    jsonify,
    flash,
    Response,
)
from flask.views import MethodView

from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.tools import capture_traceback
from src.characters.characters_manager import CharactersManager
from src.maps.algorithms.get_current_area_identifier_algorithm import (
    GetCurrentAreaIdentifierAlgorithm,
)
from src.maps.algorithms.get_place_info_algorithm import GetPlaceInfoAlgorithm
from src.maps.algorithms.get_time_and_weather_info_algorithm import (
    GetTimeAndWeatherInfoAlgorithm,
)
from src.maps.composers.get_area_info_algorithm_composer import (
    GetAreaInfoAlgorithmComposer,
)
from src.maps.composers.get_current_weather_identifier_algorithm_composer import (
    GetCurrentWeatherIdentifierAlgorithmComposer,
)
from src.maps.composers.get_location_info_algorithm_composer import (
    GetLocationInfoAlgorithmComposer,
)
from src.maps.composers.process_search_for_place_command_composer import (
    ProcessSearchForPlaceCommandComposer,
)
from src.maps.enums import (
    CardinalDirection,
)
from src.maps.exceptions import SearchForPlaceError
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.map_manager import MapManager
from src.maps.map_repository import MapRepository
from src.maps.templates_repository import TemplatesRepository
from src.movements.composers.exit_place_command_composer import ExitPlaceCommandComposer
from src.services.character_service import CharacterService
from src.services.place_service import PlaceService
from src.services.web_service import WebService
from src.time.time_manager import TimeManager

logger = logging.getLogger(__name__)


class LocationHubView(MethodView):

    @staticmethod
    def get_playthrough_name():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return None, redirect(url_for("index"))
        return playthrough_name, None

    @staticmethod
    def initialize_managers(playthrough_name):
        place_manager = PlaceManagerFactory(playthrough_name).create_place_manager()
        map_repository = MapRepository(playthrough_name)
        template_repository = TemplatesRepository()
        map_manager = MapManager(
            playthrough_name, place_manager, map_repository, template_repository
        )

        current_place = map_manager.get_current_place_template()
        current_place_type = place_manager.get_current_place_type()
        characters_manager = CharactersManager(playthrough_name)
        web_service = WebService()

        return (
            place_manager,
            map_manager,
            current_place,
            current_place_type,
            characters_manager,
            web_service,
        )

    def get(self):
        playthrough_name, redirect_response = self.get_playthrough_name()
        if redirect_response:
            return redirect_response

        (
            place_manager,
            map_manager,
            current_place,
            current_place_type,
            characters_manager,
            web_service,
        ) = self.initialize_managers(playthrough_name)

        characters_at_current_place = (
            characters_manager.get_characters_at_current_place()
        )
        web_service.format_image_urls_of_characters(characters_at_current_place)
        followers = characters_manager.get_followers()
        web_service.format_image_urls_of_characters(followers)

        map_manager = MapManagerFactory(playthrough_name).create_map_manager()
        areas = map_manager.get_all_areas()
        place_manager_factory = PlaceManagerFactory(playthrough_name)

        current_area_identifier = GetCurrentAreaIdentifierAlgorithm(
            playthrough_name, place_manager_factory
        ).do_algorithm()

        get_area_info_algorithm = GetAreaInfoAlgorithmComposer(
            playthrough_name
        ).compose_algorithm()

        get_location_info_algorithm = GetLocationInfoAlgorithmComposer(
            playthrough_name
        ).compose_algorithm()

        place_manager_factory = PlaceManagerFactory(playthrough_name)

        place_data = GetPlaceInfoAlgorithm(
            get_area_info_algorithm, get_location_info_algorithm, place_manager_factory
        ).do_algorithm()

        get_current_weather_identifier_algorithm = (
            GetCurrentWeatherIdentifierAlgorithmComposer(
                playthrough_name
            ).compose_algorithm()
        )

        time_and_weather_data = GetTimeAndWeatherInfoAlgorithm(
            playthrough_name, get_current_weather_identifier_algorithm
        ).do_algorithm()

        return render_template(
            "location-hub.html",
            current_place=current_place,
            characters=characters_at_current_place,
            followers=followers,
            place_description=session.get("place_description", ""),
            place_description_voice_line_url=session.get(
                "place_description_voice_line_url", None
            ),
            current_place_type=current_place_type,
            can_search_for_location=place_data.can_search_for_location,
            locations_present=place_data.locations_present,
            can_search_for_room=place_data.can_search_for_room,
            rooms_present=place_data.rooms_present,
            cardinal_connections=place_data.cardinal_connections,
            current_hour=time_and_weather_data.current_hour,
            current_time_of_day=time_and_weather_data.current_time_of_day,
            location_types=place_data.available_location_types,
            room_types=place_data.available_room_types,
            current_weather=time_and_weather_data.current_weather,
            current_weather_description=time_and_weather_data.current_weather_description,
            all_weathers=time_and_weather_data.all_weathers,
            weather_icon_class=time_and_weather_data.weather_icon_class,
            areas=areas,
            current_area_identifier=current_area_identifier,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Session expired. Return to the index.",
                        }
                    ),
                    400,
                )
            else:
                return redirect(url_for("index"))
        action = request.form.get("submit_action")
        if not action:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": "Action invalid."}), 400
            else:
                return redirect(url_for("location-hub"))
        method_name = WebService.create_method_name(action)
        method = getattr(self, method_name, None)
        if method:
            return method(playthrough_name)
        else:
            logger.warning(f"Method '{method_name}' not found in LocationHubView.")
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
    def handle_change_weather(playthrough_name):
        new_weather = request.form.get("weather_identifier")
        place_manager = PlaceManagerFactory(playthrough_name).create_place_manager()
        place_manager.set_current_weather(new_weather)
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_describe_place(playthrough_name):
        try:
            description, voice_line_file_name = PlaceService().describe_place(
                playthrough_name
            )
            voice_line_url = WebService.get_file_url(
                Path("voice_lines"), voice_line_file_name
            )
            PlaythroughManager(playthrough_name).add_to_adventure("\n" + description)
            session["place_description"] = description
            session["place_description_voice_line_url"] = voice_line_url
            response = {
                "success": True,
                "message": "Description generated successfully.",
                "description": description,
                "voice_line_url": voice_line_url,
            }
        except Exception as e:
            response = {
                "success": False,
                "error": f"Failed to generate the description. Error: {str(e)}",
            }
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify(response), 200
        else:
            return redirect(url_for("location-hub"))

    @staticmethod
    def handle_proceed_to_chat(_playthrough_name):
        return redirect(url_for("participants"))

    @staticmethod
    def exit_place(playthrough_name: str) -> Response:
        ExitPlaceCommandComposer(playthrough_name).compose_command().execute()
        session.pop("place_description", None)
        return redirect(url_for("location-hub"))

    def handle_exit_location(self, playthrough_name) -> Response:
        return self.exit_place(playthrough_name)

    def handle_exit_room(self, playthrough_name: str) -> Response:
        return self.exit_place(playthrough_name)

    @staticmethod
    def handle_visit_location(playthrough_name):
        location_identifier = request.form.get("location_identifier")
        PlaceService().visit_place(playthrough_name, location_identifier)
        session.pop("place_description", None)
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_enter_room(playthrough_name: str):
        room_identifier = request.form.get("room_identifier")
        PlaceService().visit_place(playthrough_name, room_identifier)
        session.pop("place_description", None)
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_advance_time_one_hour(playthrough_name):
        TimeManager(playthrough_name).advance_time(1)
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_advance_time_five_hours(playthrough_name):
        TimeManager(playthrough_name).advance_time(5)
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_advance_time_ten_hours(playthrough_name):
        TimeManager(playthrough_name).advance_time(10)
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_explore_cardinal_direction(playthrough_name):
        try:
            cardinal_direction = CardinalDirection(
                request.form.get("cardinal_direction")
            )
            result = PlaceService().create_cardinal_connection(
                playthrough_name, cardinal_direction
            )
            if not result.was_successful():
                flash(
                    f"Wasn't able to explore cardinal direction: {result.get_error()}",
                    "error",
                )
                return redirect(url_for("location-hub"))
            flash(f"Area located {cardinal_direction.value}.", "success")
        except ValueError as e:
            flash(f"Invalid cardinal direction. Error: {str(e)}", "error")
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_travel_in_cardinal_direction(_playthrough_name):
        session["destination_identifier"] = request.form.get("destination_identifier")
        return redirect(url_for("travel"))

    @staticmethod
    def handle_search_for_place(playthrough_name: str, child_place_type: TemplateType):
        try:
            ProcessSearchForPlaceCommandComposer(
                playthrough_name
            ).compose_command().execute()
        except SearchForPlaceError as e:
            flash(f"Couldn't attach {child_place_type.value}. Error: {str(e)}", "error")
        except Exception as e:
            capture_traceback()
            flash(f"Couldn't attach {child_place_type.value}. Error: {str(e)}", "error")

        return redirect(url_for("location-hub"))

    def handle_search_for_room(self, playthrough_name: str) -> Response:
        return self.handle_search_for_place(playthrough_name, TemplateType.ROOM)

    def handle_search_for_location(self, playthrough_name) -> Response:
        return self.handle_search_for_place(playthrough_name, TemplateType.LOCATION)

    @staticmethod
    def handle_teleport_to_area(playthrough_name: str):
        area_identifier = request.form.get("area_identifier")
        PlaceService().visit_place(playthrough_name, area_identifier)
        session.pop("place_description", None)
        return redirect(url_for("location-hub"))
