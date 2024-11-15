import logging

from flask import redirect, url_for, session, render_template, request, jsonify
from flask.views import MethodView
from openai import OpenAI
from swarm import Swarm

from src.base.constants import OPENROUTER_API_URL
from src.databases.chroma_db_database import ChromaDbDatabase
from src.filesystem.config_loader import ConfigLoader
from src.filesystem.file_operations import (
    remove_file,
)
from src.filesystem.path_manager import PathManager
from src.prompting.llms import Llms
from src.writers_room.agents.agents import create_agents
from src.writers_room.context_loader import ContextLoader
from src.writers_room.enums import AgentType
from src.writers_room.utils import (
    ensure_writers_room_files,
    prepare_messages,
)
from src.writers_room.writers_room_session_repository import (
    WritersRoomSessionRepository,
)

logger = logging.getLogger(__name__)


class WritersRoomView(MethodView):
    @staticmethod
    def _get_agent_key(agent_name):
        agent_name_correlation = {
            AgentType.SHOWRUNNER.value: "showrunner",
            AgentType.STORY_EDITOR.value: "story_editor",
            AgentType.CHARACTER_DEVELOPMENT.value: "character_development",
            AgentType.WORLD_BUILDING.value: "world_building",
            AgentType.CONTINUITY_MANAGER.value: "continuity_manager",
            AgentType.RESEARCHER.value: "researcher",
            AgentType.THEME.value: "theme",
            AgentType.PLOT_DEVELOPMENT.value: "plot_development",
            AgentType.PACING.value: "pacing",
        }
        return agent_name_correlation.get(agent_name, "showrunner")

    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        # Ensure necessary files and directories exist.
        ensure_writers_room_files(playthrough_name)

        # Use WritersRoomSession to handle session data
        session_manager = WritersRoomSessionRepository(playthrough_name)
        messages = session_manager.get_messages()

        # Prepare messages data for the template
        messages_data = prepare_messages(messages)

        return render_template("writers-room.html", messages=messages_data)

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            # Handle AJAX request
            action = request.form.get("submit_action")
            if action == "send":
                return self.handle_send(playthrough_name)
            elif action == "end_session":
                return self.handle_end_session(playthrough_name)
            else:
                return jsonify({"success": False, "error": "Invalid action"})
        else:
            return redirect(url_for("writers-room"))

    def handle_send(self, playthrough_name):
        user_message = request.form.get("message", "")
        if not user_message:
            return jsonify({"success": False, "error": "No message provided"})

        # Initialise Swarm client
        config_loader = ConfigLoader()

        client = Swarm(
            OpenAI(
                api_key=config_loader.load_openrouter_secret_key(),
                base_url=OPENROUTER_API_URL,
            )
        )

        # Create agents
        agents = create_agents(playthrough_name)

        # Use WritersRoomSession to handle session data
        writers_room_session_repository = WritersRoomSessionRepository(playthrough_name)
        messages = writers_room_session_repository.get_messages()

        # Append user message
        messages.append({"role": "user", "content": user_message})

        # Get current agent name
        agent_name = writers_room_session_repository.get_agent_name()

        # Try to recover the context variables from the repository.
        context_variables = writers_room_session_repository.get_context_variables()

        database = ChromaDbDatabase(playthrough_name)

        if not context_variables:
            # Prepare context variables using ContextLoader
            context_loader = ContextLoader(playthrough_name, user_message, database)
            context_variables = context_loader.load_context_variables()

        # Get agent key
        agent_key = self._get_agent_key(agent_name)
        agent = agents[agent_key]

        # Run Swarm client
        logger.info("Running Writers' Room.")
        response = client.run(
            agent=agent,
            messages=messages,
            model_override=Llms().for_writers_room().get_name(),
            context_variables=context_variables,
        )

        # Extend messages with response messages
        messages.extend(response.messages)

        # Update session data
        writers_room_session_repository.set_messages(messages)
        writers_room_session_repository.set_agent_name(response.agent.name)
        writers_room_session_repository.set_context_variables(
            response.context_variables
        )
        writers_room_session_repository.save()

        # Prepare messages data for response
        messages_data = prepare_messages(response.messages)

        return jsonify({"success": True, "messages": messages_data, "action": "send"})

    @staticmethod
    def handle_end_session(playthrough_name):
        path_manager = PathManager()
        session_path = path_manager.get_writers_room_session(playthrough_name)

        try:
            # Delete the session file
            remove_file(session_path)

            return jsonify({"success": True, "action": "end_session"})
        except Exception as e:
            logger.error(
                f"Error ending writers' room session for {playthrough_name}: {str(e)}"
            )
            return jsonify(
                {
                    "success": False,
                    "error": "Failed to end session.",
                    "action": "end_session",
                }
            )
