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

from src.base.constants import WEATHER_ICON_MAPPING
from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.tools import capture_traceback
from src.characters.characters_manager import CharactersManager
from src.maps.algorithms.get_available_place_types_algorithm import (
    GetAvailablePlaceTypesAlgorithm,
)
from src.maps.algorithms.get_current_area_identifier_algorithm import (
    GetCurrentAreaIdentifierAlgorithm,
)
from src.maps.algorithms.get_places_in_place_algorithm import GetPlacesInPlaceAlgorithm
from src.maps.commands.attach_place_command import AttachPlaceCommand
from src.maps.commands.search_for_place_command import SearchForPlaceCommand
from src.maps.composers.get_current_weather_identifier_algorithm_composer import (
    GetCurrentWeatherIdentifierAlgorithmComposer,
)
from src.maps.composers.place_selection_manager_composer import (
    PlaceSelectionManagerComposer,
)
from src.maps.composers.random_template_type_map_entry_provider_factory_composer import (
    RandomTemplateTypeMapEntryProviderFactoryComposer,
)
from src.maps.enums import (
    CardinalDirection,
)
from src.maps.exceptions import SearchForPlaceError
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.map_manager import MapManager
from src.maps.map_repository import MapRepository
from src.maps.navigation_manager import NavigationManager
from src.maps.templates_repository import TemplatesRepository
from src.maps.weathers_manager import WeathersManager
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

    @staticmethod
    def get_area_information(playthrough_name):
        map_manager = MapManagerFactory(playthrough_name).create_map_manager()
        areas = map_manager.get_all_areas()
        place_manager_factory = PlaceManagerFactory(playthrough_name)

        current_area_identifier = GetCurrentAreaIdentifierAlgorithm(
            playthrough_name, place_manager_factory
        ).do_algorithm()

        return areas, current_area_identifier

    def get_place_specific_info(
        self, playthrough_name, current_place_type, current_place
    ):
        locations_present = None
        can_search_for_location = False
        available_location_types = []
        rooms_present = None
        can_search_for_room = False
        available_room_types = []
        cardinal_connections = None

        if current_place_type == TemplateType.AREA:
            (
                locations_present,
                can_search_for_location,
                available_location_types,
                cardinal_connections,
            ) = self.handle_area_specifics(playthrough_name, current_place)

        if current_place_type == TemplateType.LOCATION:
            (
                rooms_present,
                can_search_for_room,
                available_room_types,
            ) = self.handle_location_specifics(playthrough_name, current_place)

        return (
            locations_present,
            can_search_for_location,
            available_location_types,
            rooms_present,
            can_search_for_room,
            available_room_types,
            cardinal_connections,
        )

    @staticmethod
    def handle_area_specifics(playthrough_name, current_place: str):
        playthrough_manager = PlaythroughManager(playthrough_name)

        locations_present = GetPlacesInPlaceAlgorithm(
            playthrough_name,
            playthrough_manager.get_current_place_identifier(),
            TemplateType.AREA,
            TemplateType.LOCATION,
        ).do_algorithm()

        cardinal_connections = NavigationManager(
            MapRepository(playthrough_name)
        ).get_cardinal_connections(playthrough_manager.get_current_place_identifier())

        place_selection_manager = PlaceSelectionManagerComposer(
            playthrough_name
        ).compose_manager()

        place_manager_factory = PlaceManagerFactory(playthrough_name)

        available_location_types = GetAvailablePlaceTypesAlgorithm(
            playthrough_name,
            current_place,
            TemplateType.LOCATION,
            place_manager_factory,
            place_selection_manager,
        ).do_algorithm()

        can_search_for_location = bool(available_location_types)

        return (
            locations_present,
            can_search_for_location,
            available_location_types,
            cardinal_connections,
        )

    @staticmethod
    def handle_location_specifics(playthrough_name, current_place: str):
        playthrough_manager = PlaythroughManager(playthrough_name)

        rooms_present = GetPlacesInPlaceAlgorithm(
            playthrough_name,
            playthrough_manager.get_current_place_identifier(),
            TemplateType.LOCATION,
            TemplateType.ROOM,
        ).do_algorithm()

        place_selection_manager = PlaceSelectionManagerComposer(
            playthrough_name
        ).compose_manager()

        place_manager_factory = PlaceManagerFactory(playthrough_name)

        available_room_types = GetAvailablePlaceTypesAlgorithm(
            playthrough_name,
            current_place,
            TemplateType.ROOM,
            place_manager_factory,
            place_selection_manager,
        ).do_algorithm()

        can_search_for_room = bool(available_room_types)

        return rooms_present, can_search_for_room, available_room_types

    @staticmethod
    def get_time_and_weather_info(playthrough_name):
        time_manager = TimeManager(playthrough_name)
        current_hour = time_manager.get_hour()
        current_time_of_day = time_manager.get_time_of_the_day()
        weathers_manager = WeathersManager()

        current_weather = (
            GetCurrentWeatherIdentifierAlgorithmComposer(playthrough_name)
            .compose_algorithm()
            .do_algorithm()
        )
        current_weather_description = weathers_manager.get_weather_description(
            current_weather
        )

        weather_icon_class = WEATHER_ICON_MAPPING.get(
            current_weather, "fas fa-cloud-sun"
        )

        all_weathers = weathers_manager.get_all_weather_identifiers()

        return (
            current_hour,
            current_time_of_day,
            current_weather,
            current_weather_description,
            weather_icon_class,
            all_weathers,
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

        areas, current_area_identifier = self.get_area_information(playthrough_name)

        (
            locations_present,
            can_search_for_location,
            available_location_types,
            rooms_present,
            can_search_for_room,
            available_room_types,
            cardinal_connections,
        ) = self.get_place_specific_info(
            playthrough_name,
            current_place_type,
            current_place,
        )

        (
            current_hour,
            current_time_of_day,
            current_weather,
            current_weather_description,
            weather_icon_class,
            all_weathers,
        ) = self.get_time_and_weather_info(playthrough_name)

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
            can_search_for_location=can_search_for_location,
            locations_present=locations_present,
            can_search_for_room=can_search_for_room,
            rooms_present=rooms_present,
            cardinal_connections=cardinal_connections,
            current_hour=current_hour,
            current_time_of_day=current_time_of_day,
            location_types=available_location_types,
            room_types=available_room_types,
            current_weather=current_weather,
            current_weather_description=current_weather_description,
            all_weathers=all_weathers,
            weather_icon_class=weather_icon_class,
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
            random_template_type_map_entry_provider_factory = (
                RandomTemplateTypeMapEntryProviderFactoryComposer(
                    playthrough_name
                ).compose_factory()
            )

            place_manager_factory = PlaceManagerFactory(playthrough_name)

            map_manager_factory = MapManagerFactory(playthrough_name)

            SearchForPlaceCommand(
                playthrough_name,
                random_template_type_map_entry_provider_factory,
                place_manager_factory,
                map_manager_factory,
            ).execute()

            new_id, _ = (
                map_manager_factory.create_map_manager().get_identifier_and_place_template_of_latest_map_entry()
            )

            AttachPlaceCommand(
                playthrough_name, new_id, place_manager_factory.create_place_manager()
            ).execute()
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
