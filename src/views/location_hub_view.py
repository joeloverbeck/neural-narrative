import logging

from flask import session, redirect, url_for, render_template, request, jsonify, flash
from flask.views import MethodView

from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.tools import capture_traceback
from src.characters.characters_manager import CharactersManager
from src.filesystem.config_loader import ConfigLoader
from src.maps.composers.place_selection_manager_composer import (
    PlaceSelectionManagerComposer,
)
from src.maps.composers.random_template_type_map_entry_provider_factory_composer import (
    RandomTemplateTypeMapEntryProviderFactoryComposer,
)
from src.maps.configs.cardinal_connection_creation_factory_config import (
    CardinalConnectionCreationFactoryConfig,
)
from src.maps.configs.cardinal_connection_creation_factory_factories_config import (
    CardinalConnectionCreationFactoryFactoriesConfig,
)
from src.maps.enums import (
    CardinalDirection,
    RandomTemplateTypeMapEntryCreationResultType,
)
from src.maps.factories.concrete_cardinal_connection_creation_factory import (
    ConcreteCardinalConnectionCreationFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.navigation_manager_factory import NavigationManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.map_manager import MapManager
from src.maps.map_repository import MapRepository
from src.maps.navigation_manager import NavigationManager
from src.maps.templates_repository import TemplatesRepository
from src.maps.weathers_manager import WeathersManager
from src.services.character_service import CharacterService
from src.services.place_service import PlaceService
from src.services.web_service import WebService
from src.time.time_manager import TimeManager

logger = logging.getLogger(__name__)


class LocationHubView(MethodView):

    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        place_manager = PlaceManagerFactory(playthrough_name).create_place_manager()
        map_repository = MapRepository(playthrough_name)
        template_repository = TemplatesRepository()
        map_manager = MapManager(
            playthrough_name, place_manager, map_repository, template_repository
        )
        current_place = map_manager.get_current_place_template()
        current_place_type = place_manager.get_current_place_type()
        characters_manager = CharactersManager(playthrough_name)
        characters_at_current_place = (
            characters_manager.get_characters_at_current_place()
        )
        web_service = WebService()
        web_service.format_image_urls_of_characters(characters_at_current_place)
        followers = characters_manager.get_followers()
        web_service.format_image_urls_of_characters(followers)

        locations_present = None
        cardinal_connections = None
        can_search_for_location = False
        available_location_types = []
        if current_place_type == TemplateType.AREA:
            playthrough_manager = PlaythroughManager(playthrough_name)
            locations_present = map_manager.get_locations_in_area(
                playthrough_manager.get_current_place_identifier()
            )
            cardinal_connections = NavigationManager(
                map_repository
            ).get_cardinal_connections(
                playthrough_manager.get_current_place_identifier()
            )

            place_selection_manager = PlaceSelectionManagerComposer(
                playthrough_name
            ).compose_manager()

            available_location_types = (
                place_selection_manager.get_available_location_types(current_place)
            )
            if available_location_types:
                can_search_for_location = True
        time_manager = TimeManager(playthrough_name)
        current_hour = time_manager.get_hour()
        current_time_of_day = time_manager.get_time_of_the_day()
        map_manager_factory = MapManagerFactory(playthrough_name)
        weathers_manager = WeathersManager(map_manager_factory)
        current_weather = weathers_manager.get_current_weather_identifier()
        current_weather_description = weathers_manager.get_weather_description(
            current_weather
        )
        weather_icon_mapping = {
            "sunny": "fas fa-sun",
            "rainy": "fas fa-cloud-showers-heavy",
            "cloudy": "fas fa-cloud",
            "stormy": "fas fa-cloud-bolt",
            "snowy": "fas fa-snowflake",
            "foggy": "fas fa-smog",
            "windy": "fas fa-wind",
            "misty": "fas fa-smog",
            "hail": "fas fa-cloud-rain",
            "overcast": "fas fa-cloud",
        }
        weather_icon_class = weather_icon_mapping.get(
            current_weather, "fas fa-cloud-sun"
        )
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
            cardinal_connections=cardinal_connections,
            current_hour=current_hour,
            current_time_of_day=current_time_of_day,
            location_types=available_location_types,
            current_weather=current_weather,
            current_weather_description=current_weather_description,
            all_weathers=weathers_manager.get_all_weather_identifiers(),
            weather_icon_class=weather_icon_class,
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
                "voice_lines", voice_line_file_name
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
    def handle_exit_location(playthrough_name):
        PlaceService().exit_location(playthrough_name)
        session.pop("place_description", None)
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_visit_location(playthrough_name):
        location_identifier = request.form.get("location_identifier")
        PlaceService().visit_location(playthrough_name, location_identifier)
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
        cardinal_direction = CardinalDirection(request.form.get("cardinal_direction"))

        random_template_type_map_entry_provider_factory = (
            RandomTemplateTypeMapEntryProviderFactoryComposer(
                playthrough_name
            ).compose_factory()
        )

        hierarchy_manager_factory = HierarchyManagerFactory(playthrough_name)
        map_manager_factory = MapManagerFactory(playthrough_name)
        map_repository = MapRepository(playthrough_name)
        navigation_manager_factory = NavigationManagerFactory(map_repository)
        result = ConcreteCardinalConnectionCreationFactory(
            CardinalConnectionCreationFactoryConfig(
                playthrough_name, cardinal_direction
            ),
            CardinalConnectionCreationFactoryFactoriesConfig(
                random_template_type_map_entry_provider_factory,
                hierarchy_manager_factory,
                map_manager_factory,
                navigation_manager_factory,
            ),
        ).create_cardinal_connection()

        if not result.was_successful():
            flash(
                f"Wasn't able to explore cardinal direction: {result.get_error()}",
                "error",
            )
            return redirect(url_for("location-hub"))

        flash(f"Area located {cardinal_direction.value}.", "success")
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_travel_in_cardinal_direction(_playthrough_name):
        session["destination_identifier"] = request.form.get("destination_identifier")
        return redirect(url_for("travel"))

    @staticmethod
    def handle_search_for_location(playthrough_name):
        place_manager = PlaceManagerFactory(playthrough_name).create_place_manager()
        map_manager = MapManager(
            playthrough_name,
            place_manager,
            MapRepository(playthrough_name),
            TemplatesRepository(),
        )

        father_template = map_manager.get_current_place_template()

        playthrough_manager = PlaythroughManager(playthrough_name)
        father_identifier = playthrough_manager.get_current_place_identifier()

        random_template_type_map_entry_provider = (
            RandomTemplateTypeMapEntryProviderFactoryComposer(
                playthrough_name
            ).compose_factory()
        ).create_provider(
            father_identifier, father_template, TemplateType.AREA, TemplateType.LOCATION
        )

        try:
            result = random_template_type_map_entry_provider.create_map_entry()

            if (
                result.get_result_type()
                == RandomTemplateTypeMapEntryCreationResultType.FAILURE
                or result.get_result_type()
                == RandomTemplateTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
            ):
                flash(f"Couldn't attach location. Error: {result.get_error()}", "error")
            else:
                new_id, _ = (
                    map_manager.get_identifier_and_place_template_of_latest_map_entry()
                )
                place_manager.add_location(new_id)

                config_loader = ConfigLoader()

                TimeManager(playthrough_name).advance_time(
                    config_loader.get_time_advanced_due_to_searching_for_location()
                )
        except Exception as e:
            capture_traceback()
            flash(f"Couldn't attach location. Error: {str(e)}", "error")

        return redirect(url_for("location-hub"))
