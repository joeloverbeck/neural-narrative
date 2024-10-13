from flask import redirect, session, render_template, url_for, flash, request, jsonify
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
        purpose = session.get("purpose")

        if not playthrough_name:
            return redirect(url_for("index"))

        playthrough_manager = PlaythroughManager(playthrough_name)

        if not dialogue_participants and not playthrough_manager.has_ongoing_dialogue(
            playthrough_name
        ):
            return redirect(url_for("participants"))

        filesystem_manager = FilesystemManager()

        ongoing_dialogue_file = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_ongoing_dialogue(playthrough_name)
        )

        # There is a playthrough_name in session, but the participants may not be there.
        if not dialogue_participants:
            session["participants"] = ongoing_dialogue_file["participants"]

        # There is a playthrough_name in session, but the purpose may not be there.
        if not purpose and playthrough_manager.has_ongoing_dialogue(playthrough_name):
            session["purpose"] = ongoing_dialogue_file.get("purpose", None)

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
        playthrough_name = session.get("playthrough_name")
        dialogue_participants = session.get("participants")

        if not playthrough_name or not dialogue_participants:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Session expired. Please start a new chat.",
                        }
                    ),
                    400,
                )
            else:
                return redirect(url_for("index"))

        dialogue = session.get("dialogue", [])
        action = request.form.get("submit_action")
        user_input = request.form.get("user_input")

        if action == "Send":
            if not user_input:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return (
                        jsonify({"success": False, "error": "Please enter a message."}),
                        400,
                    )
                else:
                    flash("Please enter a message.")
                    return redirect(url_for("chat"))

            dialogue_service = DialogueService()

            messages, is_goodbye = dialogue_service.process_user_input(user_input)

            if is_goodbye:
                session.pop("participants", None)
                session.pop("dialogue", None)
                session.pop("purpose", None)

                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({"success": True, "goodbye": True}), 200
                else:
                    return redirect(url_for("story-hub"))

            dialogue.extend(messages)
            if len(dialogue) > MAX_DIALOGUE_ENTRIES_FOR_WEB:
                dialogue = dialogue[-MAX_DIALOGUE_ENTRIES_FOR_WEB:]

            session["dialogue"] = dialogue

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                # Prepare messages to send back
                messages_data = []
                for msg in messages:
                    messages_data.append(
                        {
                            "alignment": msg["alignment"],
                            "message_text": msg["message_text"],
                            "sender_name": msg["sender_name"],
                            "sender_photo_url": msg["sender_photo_url"],
                            "file_url": msg["file_url"] or "",
                        }
                    )
                return jsonify({"success": True, "messages": messages_data}), 200
            else:
                return redirect(url_for("chat"))

        elif action == "Ambient narration":
            ambient_message = DialogueService().process_ambient_message()

            # Add the message to dialogue
            dialogue.append(ambient_message)
            if len(dialogue) > MAX_DIALOGUE_ENTRIES_FOR_WEB:
                dialogue = dialogue[-MAX_DIALOGUE_ENTRIES_FOR_WEB:]

            session["dialogue"] = dialogue

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                messages_data = [
                    {
                        "alignment": ambient_message["alignment"],
                        "message_text": ambient_message["message_text"],
                        "sender_name": ambient_message["sender_name"],
                        "sender_photo_url": ambient_message["sender_photo_url"],
                        "file_url": ambient_message["file_url"] or "",
                    }
                ]
                return jsonify({"success": True, "messages": messages_data}), 200
            else:
                return redirect(url_for("chat"))

        else:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": "Unknown action."}), 400
            else:
                flash("Unknown action.")
                return redirect(url_for("chat"))
