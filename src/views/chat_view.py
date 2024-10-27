import logging

from flask import redirect, session, render_template, url_for, flash, request, jsonify
from flask.views import MethodView

from src.base.tools import capture_traceback
from src.dialogues.algorithms.handle_dialogue_state_algorithm import (
    HandleDialogueStateAlgorithm,
)
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.services.dialogue_service import DialogueService
from src.time.time_manager import TimeManager

logger = logging.getLogger(__name__)


class ChatView(MethodView):

    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        dialogue_participants = session.get("participants")
        purpose = session.get("purpose")
        if not playthrough_name:
            return redirect(url_for("index"))

        product = HandleDialogueStateAlgorithm(
            playthrough_name, dialogue_participants, purpose
        ).do_algorithm()

        if not product.get_data() and not dialogue_participants:
            return redirect(url_for("participants"))

        session.update(product.get_data())

        dialogue = session.get("dialogue", [])

        time_manager = TimeManager(playthrough_name)

        current_place_template = (
            MapManagerFactory(playthrough_name)
            .create_map_manager()
            .get_current_place_template()
        )

        return render_template(
            "chat.html",
            dialogue=dialogue,
            current_time=time_manager.get_time_of_the_day(),
            current_place_template=current_place_template,
        )

    @staticmethod
    def post():
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
        event_input = request.form.get("event_input")

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

            try:
                messages, is_goodbye = dialogue_service.process_user_input(user_input)
            except Exception as e:
                capture_traceback()
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({"success": False, "error": f"Error: {str(e)}"}), 200
                else:
                    return redirect(url_for("chat"))

            if is_goodbye:
                session.pop("participants", None)
                session.pop("dialogue", None)
                session.pop("purpose", None)
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({"success": True, "goodbye": True}), 200
                else:
                    return redirect(url_for("story-hub"))
            dialogue.extend(messages)

            dialogue_service.control_size_of_messages_in_session(dialogue)

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
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
            dialogue_service = DialogueService()
            ambient_message = dialogue_service.process_ambient_message()
            dialogue.append(ambient_message)

            dialogue_service.control_size_of_messages_in_session(dialogue)

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                messages_data = [
                    {
                        "alignment": ambient_message["alignment"],
                        "message_text": ambient_message["message_text"],
                        "file_url": ambient_message["file_url"] or "",
                        "message_type": ambient_message["message_type"],
                    }
                ]
                return jsonify({"success": True, "messages": messages_data}), 200
            else:
                return redirect(url_for("chat"))
        elif action == "Event":
            if not event_input:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return (
                        jsonify({"success": False, "error": "Please enter an event."}),
                        400,
                    )
                else:
                    flash("Please enter an event.")
                    return redirect(url_for("chat"))
            dialogue_service = DialogueService()

            event_message = dialogue_service.process_event_message(event_input)

            dialogue.append(event_message)

            dialogue_service.control_size_of_messages_in_session(dialogue)

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                messages_data = [
                    {
                        "alignment": event_message["alignment"],
                        "message_text": event_message["message_text"],
                        "file_url": event_message["file_url"] or "",
                        "message_type": event_message["message_type"],
                    }
                ]
                return jsonify({"success": True, "messages": messages_data}), 200
            else:
                return redirect(url_for("chat"))
        elif request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return (
                jsonify({"success": False, "error": f"Unknown action: {action}."}),
                400,
            )
        else:
            flash("Unknown action.")
            return redirect(url_for("chat"))
