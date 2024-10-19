from flask import render_template, request, session, redirect, url_for, flash, jsonify
from flask.views import MethodView

from src.base.commands.generate_story_universe_command import (
    GenerateStoryUniverseCommand,
)
from src.base.constants import (
    STORY_UNIVERSES_TEMPLATE_FILE,
)
from src.base.factories.story_universe_factory import StoryUniverseFactory
from src.base.playthrough_manager import PlaythroughManager
from src.base.playthrough_name import RequiredString
from src.config.config_manager import ConfigManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.services.playthrough_service import PlaythroughService


class IndexView(MethodView):

    def get(self):
        filesystem_manager = FilesystemManager()

        # Existing code
        playthrough_names = filesystem_manager.get_playthrough_names()
        session.pop("no_available_templates", None)

        # New code to fetch worlds, regions, and areas
        story_universes = filesystem_manager.load_existing_or_new_json_file(
            STORY_UNIVERSES_TEMPLATE_FILE
        )

        return render_template(
            "index.html",
            playthrough_names=playthrough_names,
            story_universes=story_universes,
        )

    def post(self):
        action = request.form.get("submit_action")

        if action == "create_playthrough":
            playthrough_name = request.form["playthrough_name"]
            story_universe_template = request.form["story_universe_name"]
            player_notion = request.form.get("player_notion", "")

            try:
                PlaythroughService().create_playthrough(
                    playthrough_name, story_universe_template, player_notion
                )

                flash("Playthrough created successfully!", "success")
            except Exception as e:
                flash(f"Failed to create playthrough: {str(e)}", "error")

            return redirect(url_for("index"))
        elif action == "generate_story_universe":
            story_universe_notion = request.form["story_universe_notion"]

            try:
                produce_tool_response_strategy_factory = (
                    ProduceToolResponseStrategyFactory(
                        OpenRouterLlmClientFactory().create_llm_client(),
                        ConfigManager().get_heavy_llm(),
                    )
                )

                story_universe_factory = StoryUniverseFactory(
                    RequiredString(story_universe_notion),
                    produce_tool_response_strategy_factory,
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
                session["playthrough_name"] = playthrough_name

                playthrough_manager = PlaythroughManager(playthrough_name)

                # If turns out that there's a convo ongoing, it should redirect to the chat.
                if playthrough_manager.has_ongoing_dialogue(playthrough_name):
                    return redirect(url_for("chat"))
                else:
                    return redirect(url_for("story-hub"))
            else:
                return "Invalid playthrough selected.", 400
