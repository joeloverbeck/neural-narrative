from flask import session, redirect, url_for, render_template, request
from flask.views import MethodView

from src.characters.characters_manager import CharactersManager
from src.constants import TIME_ADVANCED_DUE_TO_SEARCHING_FOR_LOCATION
from src.enums import PlaceType
from src.maps.enums import CardinalDirection, RandomPlaceTypeMapEntryCreationResultType
from src.maps.factories.concrete_cardinal_connection_creation_factory import (
    ConcreteCardinalConnectionCreationFactory,
)
from src.maps.factories.concrete_random_place_template_based_on_categories_factory import (
    ConcreteRandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.factories.concrete_random_place_type_map_entry_creation_factory import (
    ConcreteRandomPlaceTypeMapEntryCreationFactory,
)
from src.maps.factories.create_map_entry_for_playthrough_command_factory import (
    CreateMapEntryForPlaythroughCommandFactory,
)
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

        map_manager = MapManager(playthrough_name)
        current_place = map_manager.get_current_place_template()
        current_place_type = map_manager.get_current_place_type()
        characters_manager = CharactersManager(playthrough_name)
        characters_at_current_place = (
            characters_manager.get_characters_at_current_place()
        )
        web_service = WebService()

        web_service.format_image_urls_of_characters(characters_at_current_place)
        followers = characters_manager.get_followers()
        web_service.format_image_urls_of_characters(followers)

        exploration_result_message = session.get("no_available_templates", None)

        locations_present = None
        cardinal_connections = None
        available_locations = []

        can_search_for_location = False  # New flag to indicate if searching is possible
        available_location_types = []

        if current_place_type == PlaceType.AREA:
            playthrough_manager = PlaythroughManager(playthrough_name)

            # Load locations currently present in the area
            locations_present = map_manager.get_locations_in_area(
                playthrough_manager.get_current_place_identifier()
            )

            # Load cardinal directions.
            cardinal_connections = map_manager.get_cardinal_connections(
                playthrough_manager.get_current_place_identifier()
            )

            # Determine if there are available location types for searching
            available_location_types = map_manager.get_available_location_types()
            if available_location_types:
                can_search_for_location = True

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
            place_description_voice_line_url=session.get(
                "place_description_voice_line_url", None
            ),
            current_place_type=current_place_type,
            locations_present=locations_present,
            cardinal_connections=cardinal_connections,
            current_hour=current_hour,
            current_time_of_day=current_time_of_day,
            exploration_result_message=exploration_result_message,
            location_types=available_location_types,  # Available types for searching
            can_search_for_location=can_search_for_location,  # New flag
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        action = request.form.get("action")
        if not action:
            return redirect(url_for("location-hub"))

        # Dispatch to the appropriate handler method
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
    def handle_describe_place(playthrough_name):
        description, file_url = PlaceService().describe_place(playthrough_name)

        # Add the place description to the adventure.
        PlaythroughManager(playthrough_name).add_to_adventure(description + "\n")

        session["place_description"] = description
        session["place_description_voice_line_url"] = (
            file_url  # Store the voice line URL
        )
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_proceed_to_chat(playthrough_name):
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
    def handle_advance_time(playthrough_name):
        TimeManager(playthrough_name).advance_time(5)
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_explore_cardinal_direction(playthrough_name):
        cardinal_direction = CardinalDirection(request.form.get("cardinal_direction"))

        # Now it's time to create a new map entry of an area, and link it to the previous location's cardinal direction.
        result = ConcreteCardinalConnectionCreationFactory(
            playthrough_name, cardinal_direction
        ).create_cardinal_connection()

        if not result.was_successful():
            session["no_available_templates"] = result.get_error()
            return redirect(url_for("location-hub"))

        session.pop("no_available_templates", None)
        return redirect(url_for("location-hub"))

    @staticmethod
    def handle_travel_in_cardinal_direction(playthrough_name):

        session["destination_identifier"] = request.form.get("destination_identifier")

        return redirect(url_for("travel"))

    @staticmethod
    def handle_search_for_location(playthrough_name):
        location_type = request.form.get("location_type")
        map_manager = MapManager(playthrough_name)
        father_template = map_manager.get_current_place_template()

        random_place_template_based_on_categories_factory = (
            ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
                playthrough_name, location_type
            )
        )

        playthrough_manager = PlaythroughManager(playthrough_name)

        create_map_entry_for_playthrough_command_factory = (
            CreateMapEntryForPlaythroughCommandFactory(
                playthrough_name,
                playthrough_manager.get_current_place_identifier(),
                PlaceType.LOCATION,
            )
        )

        result = ConcreteRandomPlaceTypeMapEntryCreationFactory(
            playthrough_name,
            father_template,
            PlaceType.LOCATION,
            PlaceType.AREA,
            random_place_template_based_on_categories_factory,
            create_map_entry_for_playthrough_command_factory,
        ).create_random_place_type_map_entry()

        if (
            result.get_result_type()
            == RandomPlaceTypeMapEntryCreationResultType.FAILURE
            or result.get_result_type()
            == RandomPlaceTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
        ):
            session["no_available_templates"] = result.get_error()
        else:
            session.pop("no_available_templates", None)

            # A new location has been added to the map. Must link that location to the current place.
            new_id, _ = (
                map_manager.get_identifier_and_place_template_of_latest_map_entry()
            )
            map_manager.add_location(new_id)

            # Searching for a location should also advance time.
            TimeManager(playthrough_name).advance_time(
                TIME_ADVANCED_DUE_TO_SEARCHING_FOR_LOCATION
            )

        return redirect(url_for("location-hub"))
