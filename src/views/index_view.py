import logging

from flask import render_template, request, session, redirect, url_for, jsonify
from flask.views import MethodView

from src.base.commands.generate_story_universe_command import (
    GenerateStoryUniverseCommand,
)
from src.base.enums import TemplateType
from src.base.exceptions import NoEligibleWorldsError
from src.base.factories.story_universe_factory import StoryUniverseFactory
from src.base.playthrough_manager import PlaythroughManager
from src.base.tools import capture_traceback
from src.filesystem.file_operations import create_directories
from src.filesystem.filesystem_manager import FilesystemManager
from src.filesystem.path_manager import PathManager
from src.maps.templates_repository import TemplatesRepository
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms
from src.services.playthrough_service import PlaythroughService

logger = logging.getLogger(__name__)


class IndexView(MethodView):

    @staticmethod
    def get():
        # First ensure that the playthroughs dir exists.
        create_directories(PathManager().get_playthroughs_path())

        playthrough_names = FilesystemManager().get_playthrough_names()

        story_universes = TemplatesRepository().load_templates(
            TemplateType.STORY_UNIVERSE
        )

        return render_template(
            "index.html",
            playthrough_names=playthrough_names,
            story_universes=story_universes,
        )

    @staticmethod
    def post():
        action = request.form.get("submit_action")
        if action == "create_playthrough":
            playthrough_name = request.form["playthrough_name"]
            story_universe_template = request.form["story_universe_name"]
            player_notion = request.form.get("player_notion")
            try:
                PlaythroughService().create_playthrough(
                    playthrough_name, story_universe_template, player_notion
                )
                response = {
                    "success": True,
                    "message": f"Playthrough '{playthrough_name}' created successfully.",
                }
            except NoEligibleWorldsError:
                capture_traceback()
                # Delete the partially created playthrough folder
                try:
                    PlaythroughManager(playthrough_name).delete_playthrough_folder(
                        playthrough_name
                    )
                except Exception as delete_error:
                    # Log the error but continue to return the original error message
                    logger.error(f"Error deleting playthrough folder: {delete_error}")

                response = {
                    "success": False,
                    "error": f"Failed to create playthrough: there weren't eligible worlds to fit {story_universe_template}. You should create at least one.",
                }
            except Exception as e:
                capture_traceback()
                response = {
                    "success": False,
                    "error": f"Failed to create playthrough '{playthrough_name}'. Error: {str(e)}.",
                }
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
            else:
                return redirect(url_for("index"))
        elif action == "generate_story_universe":
            story_universe_notion = request.form["story_universe_notion"]
            try:
                produce_tool_response_strategy_factory = (
                    ProduceToolResponseStrategyFactoryComposer(
                        Llms().for_story_universe_generation(),
                    ).compose_factory()
                )
                story_universe_factory = StoryUniverseFactory(
                    story_universe_notion, produce_tool_response_strategy_factory
                )
                command = GenerateStoryUniverseCommand(story_universe_factory)
                command.execute()
                response = {
                    "success": True,
                    "message": "Story universe generated successfully.",
                }
            except Exception as e:
                response = {
                    "success": False,
                    "error": f"Failed to generate story universe. Error: {str(e)}",
                }
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
            else:
                return redirect(url_for("index"))
        else:
            filesystem_manager = FilesystemManager()
            playthrough_name = request.form["playthrough_name"]
            if filesystem_manager.playthrough_exists(playthrough_name):
                # Pop the participants in session, given that we may have come from another playthrough
                session.pop("participants", None)

                session["playthrough_name"] = playthrough_name
                playthrough_manager = PlaythroughManager(playthrough_name)
                if playthrough_manager.has_ongoing_dialogue(playthrough_name):
                    return redirect(url_for("chat"))
                else:
                    return redirect(url_for("story-hub"))
            else:
                return "Invalid playthrough selected.", 400
