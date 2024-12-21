import logging
from typing import List, Optional

from flask import redirect, session, render_template, url_for, flash, request, jsonify
from flask.views import MethodView

from src.base.playthrough_manager import PlaythroughManager
from src.base.tools import capture_traceback
from src.dialogues.algorithms.extract_identifiers_from_participants_data_algorithm import (
    ExtractIdentifiersFromParticipantsDataAlgorithm,
)
from src.dialogues.algorithms.get_available_characters_algorithm import (
    GetAvailableCharactersAlgorithm,
)
from src.dialogues.algorithms.get_participant_characters_other_than_player_algorithm import (
    GetParticipantCharactersOtherThanPlayerAlgorithm,
)
from src.dialogues.algorithms.load_data_from_ongoing_dialogue_algorithm import (
    LoadDataFromOngoingDialogueAlgorithm,
)
from src.dialogues.directors.handle_dialogue_state_director import (
    HandleDialogueStateDirector,
)
from src.dialogues.enums import HandleDialogueStateAlgorithmResultType
from src.dialogues.repositories.ongoing_dialogue_repository import (
    OngoingDialogueRepository,
)
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.services.dialogue_service import DialogueService
from src.services.web_service import WebService
from src.time.time_manager import TimeManager

logger = logging.getLogger(__name__)


class ChatView(MethodView):

    @staticmethod
    def update_session_with_product_data(product):
        # Merge existing participants with new ones
        existing_participants = session.get("participants", [])
        new_participants = product.get_data().get("participants", [])
        session["participants"] = list(set(existing_participants + new_participants))

        # Careful with the purpose here.
        if "purpose" in product.get_data().keys() and product.get_data().get("purpose"):
            session["purpose"] = product.get_data().get("purpose")
        session.pop("self_reflection_text", None)
        session.pop("worldview_text", None)

    @staticmethod
    def handle_session_expired():
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Session expired.",
                    }
                ),
                400,
            )
        return redirect(url_for("index"))

    @staticmethod
    def get():
        # Retrieve essential session information
        playthrough_name, dialogue_participants, purpose = (
            session.get("playthrough_name"),
            session.get("participants", []),
            session.get("purpose"),
        )

        if not playthrough_name:
            return redirect(url_for("index"))

        # Initialize dialogue components and direct dialogue state
        load_data_algorithm = LoadDataFromOngoingDialogueAlgorithm(
            playthrough_name,
            dialogue_participants,
            purpose,
            PlaythroughManager(playthrough_name).has_ongoing_dialogue(),
        )

        extract_identifiers_algorithm = ExtractIdentifiersFromParticipantsDataAlgorithm(
            playthrough_name, dialogue_participants
        )

        product = HandleDialogueStateDirector(
            playthrough_name,
            dialogue_participants,
            load_data_algorithm,
            extract_identifiers_algorithm,
        ).direct()

        # Handle redirection cases based on dialogue state
        if (
            product.get_result_type()
            == HandleDialogueStateAlgorithmResultType.SHOULD_REDIRECT_TO_PARTICIPANTS
        ):
            return redirect(url_for("participants"))

        logger.info(
            "Handle Dialogue State product: %s\nResult type: %s",
            product.get_data(),
            product.get_result_type(),
        )

        ChatView.update_session_with_product_data(product)

        available_characters = GetAvailableCharactersAlgorithm(
            playthrough_name, dialogue_participants
        ).do_algorithm()
        WebService().format_image_urls_of_characters(available_characters)

        # Get participant characters
        participant_characters = GetParticipantCharactersOtherThanPlayerAlgorithm(
            playthrough_name, dialogue_participants
        ).do_algorithm()
        WebService().format_image_urls_of_characters(participant_characters)

        return render_template(
            "chat.html",
            dialogue=OngoingDialogueRepository(playthrough_name).get_messages(),
            current_time=TimeManager(playthrough_name).get_time_of_the_day(),
            current_place_template=MapManagerFactory(playthrough_name)
            .create_map_manager()
            .get_current_place_template(),
            available_characters=available_characters,
            participant_characters=participant_characters,
        )

    @staticmethod
    def respond_with_messages(messages, is_goodbye):
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            messages_data = [
                {
                    "alignment": msg["alignment"],
                    "message_text": msg["message_text"],
                    "thoughts": msg.get("thoughts", ""),
                    "desired_action": msg.get("desired_action", ""),
                    "message_type": msg.get("message_type", ""),
                    "sender_name": msg.get("sender_name", ""),
                    "sender_photo_url": msg.get("sender_photo_url", ""),
                    "file_url": msg.get("file_url", ""),
                }
                for msg in messages
            ]

            # If it's goodbye, then we must clear out the session.
            if is_goodbye:
                session.pop("participants", None)
                session.pop("purpose", None)

            return (
                jsonify(
                    {"success": True, "messages": messages_data, "goodbye": is_goodbye}
                ),
                200,
            )
        else:
            return redirect(url_for("chat"))

    @staticmethod
    def process_action(
        playthrough_name: str,
        action,
        dialogue_participants: List[str],
        user_input=None,
        event_input=None,
        action_input=None,
    ):
        dialogue_service = DialogueService()

        if action == "Send":
            return ChatView.handle_send(
                playthrough_name, dialogue_service, user_input, dialogue_participants
            )
        elif action == "Stay Silent":
            return ChatView.handle_send(
                playthrough_name, dialogue_service, "silent", dialogue_participants
            )
        elif action == "Goodbye":
            return ChatView.handle_send(
                playthrough_name, dialogue_service, "goodbye", dialogue_participants
            )
        elif action == "Ambient narration":
            return ChatView.handle_ambient_narration(
                playthrough_name, dialogue_service, dialogue_participants
            )
        elif action == "Event":
            return ChatView.handle_event(
                playthrough_name, dialogue_service, event_input, dialogue_participants
            )
        elif action == "Grow event":
            return ChatView.handle_grow_event(
                playthrough_name, dialogue_service, event_input, dialogue_participants
            )
        elif action == "Confrontation round":
            return ChatView.handle_confrontation_round(
                playthrough_name, dialogue_service, action_input, dialogue_participants
            )
        elif action == "Narrative beat":
            return ChatView.handle_narrative_beat(
                playthrough_name, dialogue_service, dialogue_participants
            )

        raise ValueError(f"Unknown action: {action}")

    @staticmethod
    def handle_error(exception):
        capture_traceback()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": False, "error": f"Error: {str(exception)}"}), 200
        return redirect(url_for("chat"))

    @staticmethod
    def handle_unknown_action():
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": False, "error": "Unknown action."}), 400
        flash("Unknown action.")
        return redirect(url_for("chat"))

    @staticmethod
    def handle_send(
        playthrough_name: str, dialogue_service, user_input, dialogue_participants
    ):
        if not user_input:
            raise ValueError("Please enter a message.")

        messages, is_goodbye = dialogue_service.process_user_input(
            user_input, dialogue_participants
        )

        if not is_goodbye:
            ongoing_dialogue_repository = OngoingDialogueRepository(playthrough_name)

            ongoing_dialogue_repository.add_messages(messages)

            # Store latest thoughts and desired action
            for message in messages:
                sender_identifier = message.get("sender_identifier")

                # It could be that there's no sender identifier, as in the case of player dialogue,
                # because that data would only be used for storing thoughts and desired action,
                # which aren't produced by the user.
                if not sender_identifier:
                    continue

                ongoing_dialogue_repository.set_latest_thoughts(
                    sender_identifier, message["thoughts"]
                )
                ongoing_dialogue_repository.set_latest_desired_action(
                    sender_identifier, message["desired_action"]
                )

        return messages, is_goodbye

    @staticmethod
    def handle_ambient_narration(
        playthrough_name: str, dialogue_service, dialogue_participants
    ):
        ambient_message = dialogue_service.process_ambient_message(
            dialogue_participants, session.get("purpose", "")
        )

        OngoingDialogueRepository(playthrough_name).add_messages([ambient_message])

        return [ambient_message], False

    @staticmethod
    def handle_event(
        playthrough_name: str, dialogue_service, event_input, dialogue_participants
    ):
        if not event_input:
            raise ValueError("Please enter an event.")
        event_message = dialogue_service.process_event_message(
            dialogue_participants, session.get("purpose", ""), event_input
        )

        OngoingDialogueRepository(playthrough_name).add_messages([event_message])

        return [event_message], False

    @staticmethod
    def handle_grow_event(
        playthrough_name: str,
        dialogue_service: DialogueService,
        event_input: Optional[str],
        dialogue_participants: List[str],
    ):
        if not event_input:
            raise ValueError("Please enter the seed of the event.")

        event_message = dialogue_service.process_grow_event_message(
            dialogue_participants, session.get("purpose", ""), event_input
        )

        OngoingDialogueRepository(playthrough_name).add_messages([event_message])

        return [event_message], False

    @staticmethod
    def handle_confrontation_round(
        playthrough_name: str,
        dialogue_service: DialogueService,
        action_input: Optional[str],
        dialogue_participants: List[str],
    ):
        if not action_input:
            raise ValueError("Please enter the context of the action.")

        event_message = dialogue_service.process_confrontation_round(
            dialogue_participants, session.get("purpose", ""), action_input
        )

        OngoingDialogueRepository(playthrough_name).add_messages([event_message])

        return [event_message], False

    @staticmethod
    def handle_narrative_beat(
        playthrough_name: str, dialogue_service, dialogue_participants
    ):
        narrative_beat_message = dialogue_service.process_narrative_beat(
            dialogue_participants, session.get("purpose", "")
        )

        OngoingDialogueRepository(playthrough_name).add_messages(
            [narrative_beat_message]
        )

        return [narrative_beat_message], False

    @staticmethod
    def post():
        playthrough_name, dialogue_participants = session.get(
            "playthrough_name"
        ), session.get("participants")
        if not playthrough_name or not dialogue_participants:
            return ChatView.handle_session_expired()

        action = request.form.get("submit_action")
        user_input, event_input, action_input = (
            request.form.get("user_input"),
            request.form.get("event_input"),
            request.form.get("action_input"),
        )

        if action:
            try:
                # There are two types of actions: one that produce one or more messages for the chat,
                # Or actions that don't produce messages in the chat.
                if action == "Brainstorm events":
                    # The user wants to delegate brainstorming events to show them under the chat window.
                    product = DialogueService().process_brainstorm_events(
                        dialogue_participants
                    )

                    if not product.is_valid():
                        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                            return (
                                jsonify(
                                    {
                                        "success": False,
                                        "error": f"Failed to brainstorm events. Error: {product.get_error()}",
                                    }
                                ),
                                200,
                            )
                        return redirect(url_for("chat"))

                    # The product is valid.
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return (
                            jsonify(
                                {"success": True, "brainstormed_events": product.get()}
                            ),
                            200,
                        )
                    else:
                        return redirect(url_for("chat"))

                messages, is_goodbye = ChatView.process_action(
                    playthrough_name,
                    action,
                    dialogue_participants,
                    user_input,
                    event_input,
                    action_input,
                )
                return ChatView.respond_with_messages(messages, is_goodbye)
            except Exception as e:
                return ChatView.handle_error(e)
        return ChatView.handle_unknown_action()
