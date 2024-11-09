from flask import request, session, jsonify
from flask.views import MethodView

from src.base.playthrough_manager import PlaythroughManager
from src.services.dialogue_service import DialogueService


class RemoveParticipantsView(MethodView):
    @staticmethod
    def post():
        selected_characters = request.form.getlist("selected_characters")
        if not selected_characters:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Please select at least one character to remove.",
                    }
                ),
                200,
            )

        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return jsonify({"success": False, "error": "Session expired."}), 400

        current_participants = session.get("participants", [])
        playthrough_manager = PlaythroughManager(playthrough_name)
        protagonist_identifier = playthrough_manager.get_player_identifier()

        # Exclude protagonist from current participants
        current_participant_identifiers = [
            identifier
            for identifier in current_participants
            if identifier != protagonist_identifier
        ]

        # Check that selected_characters are among current participants
        invalid_characters = [
            char_id
            for char_id in selected_characters
            if char_id not in current_participant_identifiers
        ]

        if invalid_characters:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Invalid characters selected: {invalid_characters}",
                    }
                ),
                200,
            )

        try:
            DialogueService().remove_participants_from_dialogue(
                playthrough_name, selected_characters
            )
        except Exception as e:
            return (
                jsonify({"success": False, "error": f"An error occurred: {str(e)}"}),
                200,
            )

        return (
            jsonify({"success": True, "message": "Participants removed successfully."}),
            200,
        )
