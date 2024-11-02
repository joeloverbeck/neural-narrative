import logging
from typing import List, Dict

from flask import redirect, url_for, session, render_template, request, jsonify
from flask.views import MethodView
from openai import OpenAI
from swarm import Swarm

from src.base.constants import OPENROUTER_API_URL
from src.concepts.enums import ConceptType
from src.filesystem.config_loader import ConfigLoader
from src.filesystem.file_operations import (
    read_json_file,
    write_json_file,
    read_file,
    remove_file,
)
from src.filesystem.path_manager import PathManager
from src.maps.composers.places_descriptions_provider_composer import (
    PlacesDescriptionsProviderComposer,
)
from src.prompting.llms import Llms
from src.writers_room.agents.agents import create_agents
from src.writers_room.utils import (
    ensure_writers_room_files,
    prepare_messages_for_template,
)

logger = logging.getLogger(__name__)


class WritersRoomView(MethodView):

    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        # Ensure necessary files and directories exist.
        ensure_writers_room_files(playthrough_name)

        path_manager = PathManager()

        # Read the messages from the session file
        session_file = read_json_file(
            path_manager.get_writers_room_session(playthrough_name)
        )

        messages = session_file.get("messages", [])

        # Prepare messages data for the template
        messages_data = prepare_messages_for_template(messages)

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

    @staticmethod
    def handle_send(playthrough_name):
        user_message = request.form.get("message", "")
        if not user_message:
            return jsonify({"success": False, "error": "No message provided"})

        # Initialise Swarm client and run conversation
        config_loader = ConfigLoader()

        client = Swarm(
            OpenAI(
                api_key=config_loader.load_openrouter_secret_key(),
                base_url=OPENROUTER_API_URL,
            )
        )

        agents = create_agents(playthrough_name)

        # If there is a "messages" key in the session.json file of the corresponding writer's room, then we should load those messages.
        path_manager = PathManager()

        session_file = read_json_file(
            path_manager.get_writers_room_session(playthrough_name)
        )

        messages: List[Dict[str, str]] = []

        if "messages" in session_file:
            messages = session_file["messages"]

        messages.append({"role": "user", "content": user_message})

        context_file = read_file(
            path_manager.get_writers_room_context_path(playthrough_name)
        )

        facts_file = read_file(path_manager.get_facts_path(playthrough_name))

        characters_file = read_json_file(
            path_manager.get_characters_file_path(playthrough_name)
        )

        places_descriptions = (
            PlacesDescriptionsProviderComposer(playthrough_name)
            .compose_provider()
            .get_information()
        )

        concepts_file = read_json_file(
            path_manager.get_concepts_file_path(playthrough_name)
        )

        # Load context data
        context_variables = {
            "context": context_file,
            "facts": facts_file,
            "characters": characters_file,
            "places_descriptions": places_descriptions,
            ConceptType.PLOT_BLUEPRINTS.value: concepts_file[
                ConceptType.PLOT_BLUEPRINTS.value
            ],
            ConceptType.GOALS.value: concepts_file[ConceptType.GOALS.value],
            ConceptType.PLOT_TWISTS.value: concepts_file[ConceptType.PLOT_TWISTS.value],
            ConceptType.SCENARIOS.value: concepts_file[ConceptType.SCENARIOS.value],
            ConceptType.DILEMMAS.value: concepts_file[ConceptType.DILEMMAS.value],
        }

        logger.info("Running Writers' Room.")
        response = client.run(
            agent=agents["showrunner"],
            messages=messages,
            model_override=Llms().for_writers_room().get_name(),
            context_variables=context_variables,
        )

        # Append the response message to the ongoing messages
        latest_message = response.messages[-1]

        messages.append(latest_message)

        # Write the messages to file.
        session_file["messages"] = messages

        write_json_file(
            path_manager.get_writers_room_session(playthrough_name), session_file
        )

        messages_data = [
            {
                "message_text": latest_message["content"],
                "message_type": latest_message["sender"],
            }
        ]

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
