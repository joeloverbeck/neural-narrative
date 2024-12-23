import logging

from flask import (
    render_template,
    redirect,
    url_for,
    request,
    session,
    flash,
)
from flask.views import MethodView

from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.maps.algorithms.get_all_place_types_in_map_algorithm import (
    GetAllPlaceTypesInMapAlgorithm,
)
from src.maps.composers.create_map_entry_for_playthrough_command_provider_factory_composer import (
    CreateMapEntryForPlaythroughCommandProviderFactoryComposer,
)
from src.maps.factories.get_available_place_types_algorithm_composer import (
    GetAvailablePlaceTypesAlgorithmComposer,
)
from src.maps.factories.structure_options_for_attaching_places_algorithm_factory import (
    StructureOptionsForAttachingPlacesAlgorithmFactory,
)

logger = logging.getLogger(__name__)


class AttachPlacesView(MethodView):
    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        story_universe_template = PlaythroughManager(
            playthrough_name
        ).get_story_universe_template()

        available_worlds = (
            GetAvailablePlaceTypesAlgorithmComposer(
                playthrough_name,
                story_universe_template,
                TemplateType.STORY_UNIVERSE,
                TemplateType.WORLD,
            )
            .compose_algorithm()
            .do_algorithm()
        )

        available_regions = (
            GetAvailablePlaceTypesAlgorithmComposer(
                playthrough_name,
                story_universe_template,
                TemplateType.STORY_UNIVERSE,
                TemplateType.REGION,
            )
            .compose_algorithm()
            .do_algorithm()
        )

        available_areas = (
            GetAvailablePlaceTypesAlgorithmComposer(
                playthrough_name,
                story_universe_template,
                TemplateType.STORY_UNIVERSE,
                TemplateType.AREA,
            )
            .compose_algorithm()
            .do_algorithm()
        )

        available_locations = (
            GetAvailablePlaceTypesAlgorithmComposer(
                playthrough_name,
                story_universe_template,
                TemplateType.STORY_UNIVERSE,
                TemplateType.LOCATION,
            )
            .compose_algorithm()
            .do_algorithm()
        )

        available_rooms = (
            GetAvailablePlaceTypesAlgorithmComposer(
                playthrough_name,
                story_universe_template,
                TemplateType.STORY_UNIVERSE,
                TemplateType.ROOM,
            )
            .compose_algorithm()
            .do_algorithm()
        )

        worlds_in_map = GetAllPlaceTypesInMapAlgorithm(
            playthrough_name, TemplateType.WORLD
        ).do_algorithm()
        regions_in_map = GetAllPlaceTypesInMapAlgorithm(
            playthrough_name, TemplateType.REGION
        ).do_algorithm()
        areas_in_map = GetAllPlaceTypesInMapAlgorithm(
            playthrough_name, TemplateType.AREA
        ).do_algorithm()
        locations_in_map = GetAllPlaceTypesInMapAlgorithm(
            playthrough_name, TemplateType.LOCATION
        ).do_algorithm()

        # Prepare data for template
        return render_template(
            "attach-places.html",
            available_worlds=StructureOptionsForAttachingPlacesAlgorithmFactory.create_algorithm(
                available_worlds, "name", "name"
            ).do_algorithm(),
            worlds_in_map=StructureOptionsForAttachingPlacesAlgorithmFactory.create_algorithm(
                worlds_in_map, "identifier", "place_template"
            ).do_algorithm(),
            available_regions=StructureOptionsForAttachingPlacesAlgorithmFactory.create_algorithm(
                available_regions, "name", "name"
            ).do_algorithm(),
            regions_in_map=StructureOptionsForAttachingPlacesAlgorithmFactory.create_algorithm(
                regions_in_map, "identifier", "place_template"
            ).do_algorithm(),
            available_areas=StructureOptionsForAttachingPlacesAlgorithmFactory.create_algorithm(
                available_areas, "name", "name"
            ).do_algorithm(),
            areas_in_map=StructureOptionsForAttachingPlacesAlgorithmFactory.create_algorithm(
                areas_in_map, "identifier", "place_template"
            ).do_algorithm(),
            available_locations=StructureOptionsForAttachingPlacesAlgorithmFactory.create_algorithm(
                available_locations
            ).do_algorithm(),
            locations_in_map=StructureOptionsForAttachingPlacesAlgorithmFactory.create_algorithm(
                locations_in_map, "identifier", "place_template"
            ).do_algorithm(),
            available_rooms=StructureOptionsForAttachingPlacesAlgorithmFactory.create_algorithm(
                available_rooms
            ).do_algorithm(),  # No 'name' attributes
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        action = request.form.get("submit_action")
        if not action:
            return redirect(url_for("attach-places"))

        if action == "Attach World":
            return self.handle_attach_world(playthrough_name)
        elif action == "Attach Region":
            return self.handle_attach_region(playthrough_name)
        elif action == "Attach Area":
            return self.handle_attach_area(playthrough_name)
        elif action == "Attach Location":
            return self.handle_attach_location(playthrough_name)
        elif action == "Attach Room":
            return self.handle_attach_room(playthrough_name)
        else:
            logger.warning(f"Unknown action '{action}' in PlacesView.")
            return redirect(url_for("attach-places"))

    @staticmethod
    def handle_attach_world(playthrough_name):
        world_template = request.form.get("world_template")
        if not world_template:
            flash("No world selected.", "error")
            return redirect(url_for("attach-places"))

        try:
            CreateMapEntryForPlaythroughCommandProviderFactoryComposer(
                playthrough_name
            ).create_factory().create_provider(None, TemplateType.WORLD).create_command(
                world_template
            ).execute()
            flash(f"World '{world_template}' attached successfully.", "success")
        except Exception as e:
            logger.exception("Error attaching world.")
            flash(f"Error attaching world: {str(e)}", "error")
        return redirect(url_for("attach-places"))

    @staticmethod
    def handle_attach_region(playthrough_name):
        world_identifier = request.form.get("world_identifier")
        region_template = request.form.get("region_template")
        if not world_identifier or not region_template:
            flash("World or region not selected.", "error")
            return redirect(url_for("attach-places"))

        try:
            CreateMapEntryForPlaythroughCommandProviderFactoryComposer(
                playthrough_name
            ).create_factory().create_provider(
                world_identifier, TemplateType.REGION
            ).create_command(
                region_template
            ).execute()
            flash(
                f"Region '{region_template}' attached to world successfully.", "success"
            )
        except Exception as e:
            logger.exception("Error attaching region.")
            flash(f"Error attaching region: {str(e)}", "error")
        return redirect(url_for("attach-places"))

    @staticmethod
    def handle_attach_area(playthrough_name):
        region_identifier = request.form.get("region_identifier")
        area_template = request.form.get("area_template")
        if not region_identifier or not area_template:
            flash("Region or area not selected.", "error")
            return redirect(url_for("attach-places"))

        try:
            CreateMapEntryForPlaythroughCommandProviderFactoryComposer(
                playthrough_name
            ).create_factory().create_provider(
                region_identifier, TemplateType.AREA
            ).create_command(
                area_template
            ).execute()
            flash(f"Area '{area_template}' attached to region successfully.", "success")
        except Exception as e:
            logger.exception("Error attaching area.")
            flash(f"Error attaching area: {str(e)}", "error")
        return redirect(url_for("attach-places"))

    @staticmethod
    def handle_attach_location(playthrough_name):
        area_identifier = request.form.get("area_identifier")
        location_template = request.form.get("location_template")
        if not area_identifier or not location_template:
            flash("Area or location not selected.", "error")
            return redirect(url_for("attach-places"))

        try:
            CreateMapEntryForPlaythroughCommandProviderFactoryComposer(
                playthrough_name
            ).create_factory().create_provider(
                area_identifier, TemplateType.LOCATION
            ).create_command(
                location_template
            ).execute()
            flash(
                f"Location '{location_template}' attached to area successfully.",
                "success",
            )
        except Exception as e:
            logger.exception("Error attaching location.")
            flash(f"Error attaching location: {str(e)}", "error")
        return redirect(url_for("attach-places"))

    @staticmethod
    def handle_attach_room(playthrough_name):
        location_identifier = request.form.get("location_identifier")
        room_template = request.form.get("room_template")

        if not location_identifier or not room_template:
            flash("Location or room not selected.", "error")
            return redirect(url_for("attach-places"))

        try:
            CreateMapEntryForPlaythroughCommandProviderFactoryComposer(
                playthrough_name
            ).create_factory().create_provider(
                location_identifier, TemplateType.ROOM
            ).create_command(
                room_template
            ).execute()
            flash(
                f"Room '{room_template}' attached to location successfully.", "success"
            )
        except Exception as e:
            logger.exception("Error attaching room.")
            flash(f"Error attaching room: {str(e)}", "error")
        return redirect(url_for("attach-places"))
