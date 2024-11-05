import logging

from flask import request, session, redirect, url_for, render_template
from flask.views import MethodView

from src.characters.characters_manager import CharactersManager
from src.services.web_service import WebService

logger = logging.getLogger(__name__)


class ParticipantsView(MethodView):
    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        characters_manager = CharactersManager(playthrough_name)
        characters = characters_manager.get_characters_at_current_place_plus_followers()
        WebService().format_image_urls_of_characters(characters)
        if not characters:
            message = "There are no characters at your current location."
            return render_template("participants.html", characters=[], message=message)
        return render_template("participants.html", characters=characters)

    @staticmethod
    def post():
        selected_characters = request.form.getlist("selected_characters")
        purpose = request.form.get("purpose", "")
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        characters_manager = CharactersManager(playthrough_name)
        if len(selected_characters) < 1:
            error = "Please select at least one character."
            characters = (
                characters_manager.get_characters_at_current_place_plus_followers()
            )
            WebService().format_image_urls_of_characters(characters)
            return render_template(
                "participants.html", characters=characters, error=error
            )
        session["participants"] = selected_characters
        session["purpose"] = purpose

        logger.info("Purpose stored in session: %s", session.get("purpose"))

        session.pop("place_description", None)
        return redirect(url_for("chat"))
