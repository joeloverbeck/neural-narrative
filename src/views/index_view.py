from flask import render_template, request, session, redirect, url_for, flash
from flask.views import MethodView

from src.constants import (
    WORLD_TEMPLATES_FILE,
    REGIONS_TEMPLATES_FILE,
    AREAS_TEMPLATES_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.playthrough_manager import PlaythroughManager
from src.services.place_service import PlaceService
from src.services.playthrough_service import PlaythroughService


class IndexView(MethodView):

    def get(self):
        filesystem_manager = FilesystemManager()

        # Existing code
        playthrough_names = filesystem_manager.get_playthrough_names()
        session.pop("no_available_templates", None)

        # New code to fetch worlds, regions, and areas
        worlds = filesystem_manager.load_existing_or_new_json_file(WORLD_TEMPLATES_FILE)
        regions = filesystem_manager.load_existing_or_new_json_file(
            REGIONS_TEMPLATES_FILE
        )
        areas = filesystem_manager.load_existing_or_new_json_file(AREAS_TEMPLATES_FILE)

        return render_template(
            "index.html",
            playthrough_names=playthrough_names,
            worlds=worlds,
            regions=regions,
            areas=areas,
        )

    def post(self):
        form_type = request.form.get("form_type")

        if form_type == "create_playthrough":
            playthrough_name = request.form["playthrough_name_for_creation"]
            world_template = request.form["world_name"]
            player_notion = request.form.get("player_notion", "")

            try:
                PlaythroughService().create_playthrough(
                    playthrough_name, world_template, player_notion
                )

                flash("Playthrough created successfully!", "success")
            except Exception as e:
                flash(f"Failed to create playthrough: {str(e)}", "error")

            return redirect(url_for("index"))

        elif form_type == "generate_world":
            world_notion = request.form["world_notion"]

            try:
                place_service = PlaceService()
                place_service.generate_world(world_notion)
                flash("World generated successfully!", "success")
            except Exception as e:
                flash(f"World generation failed: {str(e)}", "error")
            return redirect(url_for("index"))
        elif form_type == "generate_region":
            world_name = request.form["world_name"]
            region_notion = request.form.get("region_notion", "")
            try:
                place_service = PlaceService()
                place_service.generate_region(world_name, region_notion)
                flash("Region generated successfully!", "success")
            except Exception as e:
                flash(f"Region generation failed: {str(e)}", "error")
            return redirect(url_for("index"))
        elif form_type == "generate_area":
            region_name = request.form["region_name"]
            area_notion = request.form.get("area_notion", "")
            try:
                place_service = PlaceService()
                place_service.generate_area(region_name, area_notion)
                flash("Area generated successfully!", "success")
            except Exception as e:
                flash(f"Area generation failed: {str(e)}", "error")
            return redirect(url_for("index"))
        elif form_type == "generate_location":
            area_name = request.form["area_name"]
            location_notion = request.form.get("location_notion", "")
            try:
                place_service = PlaceService()
                place_service.generate_location(area_name, location_notion)
                flash("Location generated successfully!", "success")
            except Exception as e:
                flash(f"Location generation failed: {str(e)}", "error")
            return redirect(url_for("index"))
        else:
            filesystem_manager = FilesystemManager()

            playthrough_name = request.form["playthrough_name"]

            if filesystem_manager.playthrough_exists(playthrough_name):
                session["playthrough_name"] = playthrough_name

                playthrough_manager = PlaythroughManager(playthrough_name)

                # If turns out that there's a convo ongoing, it shouldn't redirect to choose the participants.
                if playthrough_manager.has_ongoing_dialogue(playthrough_name):
                    return redirect(url_for("chat"))
                else:
                    return redirect(url_for("story-hub"))
            else:
                return "Invalid playthrough selected.", 400
