from flask import request, session, jsonify
from flask.views import MethodView


class AddParticipantsView(MethodView):
    @staticmethod
    def post():
        selected_characters = request.form.getlist("selected_characters")
        if not selected_characters:
            return (
                jsonify(
                    {"success": False, "error": "Please select at least one character."}
                ),
                200,
            )

        current_participants = session.get("participants", [])
        # Update the session participants
        session["participants"] = current_participants + selected_characters
        session.modified = True  # Ensure session is saved

        return (
            jsonify({"success": True, "message": "Participants added successfully."}),
            200,
        )
