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

        worlds_in_map = GetAllPlaceTypesInMapAlgorithm(
            playthrough_name, TemplateType.WORLD
        ).do_algorithm()
        regions_in_map = GetAllPlaceTypesInMapAlgorithm(
            playthrough_name, TemplateType.REGION
        ).do_algorithm()

        # Prepare data for template
        return render_template(
            "attach-places.html",
            available_worlds=available_worlds,
            worlds_in_map=worlds_in_map,
            available_regions=available_regions,
            regions_in_map=regions_in_map,
            available_areas=available_areas,
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
