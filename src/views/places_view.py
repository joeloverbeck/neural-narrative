import logging

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask.views import MethodView

from src.base.enums import TemplateType
from src.base.tools import capture_traceback
from src.maps.templates_repository import TemplatesRepository
from src.services.place_service import PlaceService

logger = logging.getLogger(__name__)


class PlacesView(MethodView):
    @staticmethod
    def get():
        templates_repository = TemplatesRepository()

        story_universes = templates_repository.load_templates(
            TemplateType.STORY_UNIVERSE
        )
        worlds = templates_repository.load_templates(TemplateType.WORLD)
        regions = templates_repository.load_templates(TemplateType.REGION)
        areas = templates_repository.load_templates(TemplateType.AREA)

        return render_template(
            "places.html",
            story_universes=story_universes,
            worlds=worlds,
            regions=regions,
            areas=areas,
        )

    @staticmethod
    def post():
        action = request.form.get("submit_action")
        action_configs = {
            "generate_world": {
                "params": [("story_universe_name", None), ("world_notion", None)],
                "father_place_param": "story_universe_name",
                "notion_param": "world_notion",
                "template_type": TemplateType.WORLD,
                "success_message": "World generated successfully.",
                "error_message": "Failed to generate world.",
                "redirect_url": "story-hub",
                "use_flash": False,
            },
            "generate_region": {
                "params": [("world_name", None), ("region_notion", "")],
                "father_place_param": "world_name",
                "notion_param": "region_notion",
                "template_type": TemplateType.REGION,
                "success_message": "Region generated successfully.",
                "error_message": "Failed to generate region..",
                "redirect_url": "places",
                "use_flash": True,
            },
            "generate_area": {
                "params": [("region_name", None), ("area_notion", "")],
                "father_place_param": "region_name",
                "notion_param": "area_notion",
                "template_type": TemplateType.AREA,
                "success_message": "Area generated successfully.",
                "error_message": "Failed to generate area.",
                "redirect_url": "places",
                "use_flash": True,
            },
            "generate_location": {
                "params": [("area_name", None), ("location_notion", "")],
                "father_place_param": "area_name",
                "notion_param": "location_notion",
                "template_type": TemplateType.LOCATION,
                "success_message": "Location generated successfully.",
                "error_message": "Failed to generate location.",
                "redirect_url": "story-hub",
                "use_flash": False,
            },
        }
        action_config = action_configs.get(action)
        if action_config:
            params = {}
            try:
                for param_name, default_value in action_config["params"]:
                    if default_value is None:
                        param_value = request.form[param_name]
                    else:
                        param_value = request.form.get(param_name, default_value)
                    params.update({param_name: param_value})
                father_place_name = params[action_config["father_place_param"]]
                notion = params[action_config["notion_param"]]
                template_type = action_config["template_type"]
                place_service = PlaceService()
                place_service.run_generate_place_command(
                    father_place_name, template_type, notion
                )
                response = {
                    "success": True,
                    "message": action_config["success_message"],
                }
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(response)
                else:
                    if action_config.get("use_flash", False):
                        flash(action_config["success_message"], "success")
                    return redirect(url_for(action_config["redirect_url"]))
            except KeyError as e:
                capture_traceback()
                error_message = f"Missing required parameter: {e.args[0]}"
                logger.error(error_message)
                response = {"success": False, "error": error_message}
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(response)
                else:
                    if action_config.get("use_flash", False):
                        flash(error_message, "error")
                    return redirect(url_for(action_config["redirect_url"]))
            except Exception as e:
                error_message = f"{action_config['error_message']} Error: {str(e)}"
                logger.error(error_message)
                response = {"success": False, "error": error_message}
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(response)
                else:
                    if action_config.get("use_flash", False):
                        flash(f"{action_config['error_message']}: {str(e)}", "error")
                    return redirect(url_for(action_config["redirect_url"]))
        else:
            response = {"success": False, "error": f"Unknown action: {action}"}
            logger.error(response["error"])
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response), 400
            else:
                flash(response["error"], "error")
                return redirect(url_for("places"))
