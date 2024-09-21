from flask import redirect, session, render_template, url_for, flash, request
from flask.views import MethodView

from src.constants import MAX_DIALOGUE_ENTRIES_FOR_WEB
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.services.dialogue_service import DialogueService
from src.time.time_manager import TimeManager


class ChatView(MethodView):
    def get(self):
        # Handle GET request
        playthrough_name = session.get("playthrough_name")
        dialogue_participants = session.get("participants")

        if not playthrough_name:
            return redirect(url_for("index"))

        # There is a playthrough_name in session, but the participants may not be there.
        if not dialogue_participants and PlaythroughManager(
            playthrough_name
        ).has_ongoing_dialogue(playthrough_name):
            filesystem_manager = FilesystemManager()

            session["participants"] = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_ongoing_dialogue(playthrough_name)
            )["participants"]

            dialogue_participants = session.get("participants")

        dialogue = session.get("dialogue", [])

        time_manager = TimeManager(playthrough_name)
        map_manager = MapManager(playthrough_name)
        current_place_template = map_manager.get_current_place_template()

        return render_template(
            "chat.html",
            dialogue=dialogue,
            current_time=time_manager.get_time_of_the_day(),
            current_place_template=current_place_template,
        )

    def post(self):
        # Handle POST request
        playthrough_name = session.get("playthrough_name")
        dialogue_participants = session.get("participants")

        if not playthrough_name or not dialogue_participants:
            return redirect(url_for("index"))

        dialogue = session.get("dialogue", [])
        user_input = request.form.get("user_input")

        if not user_input:
            flash("Please enter a message.")
            return redirect(url_for("chat"))

        # Process the dialogue
        dialogue_service = DialogueService(playthrough_name, dialogue_participants)

        messages, is_goodbye = dialogue_service.process_user_input(user_input)

        if is_goodbye:
            session.pop("playthrough_name", None)
            session.pop("participants", None)
            session.pop("dialogue", None)

            return redirect(url_for("index"))

        # Update dialogue
        dialogue.extend(messages)
        if len(dialogue) > MAX_DIALOGUE_ENTRIES_FOR_WEB:
            dialogue = dialogue[-MAX_DIALOGUE_ENTRIES_FOR_WEB:]

        session["dialogue"] = dialogue

        return redirect(url_for("chat"))
