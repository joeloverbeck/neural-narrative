import logging
from typing import List

from flask import request, session, redirect, url_for, render_template
from flask.views import MethodView

from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.services.web_service import WebService

logger = logging.getLogger(__name__)


class ParticipantsView(MethodView):
    @staticmethod
    def _get_possible_characters_for_chat(playthrough_name: str) -> List[Character]:
        characters_manager = CharactersManager(playthrough_name)
        characters = characters_manager.get_all_characters()

        # Must cull the player character from the possible participants.
        player_identifier = PlaythroughManager(playthrough_name).get_player_identifier()

        characters = characters_manager.get_characters(
            [
                entry["identifier"]
                for entry in characters
                if entry["identifier"] != player_identifier
            ]
        )

        WebService().format_image_urls_of_characters(characters)

        return characters

    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        characters = self._get_possible_characters_for_chat(playthrough_name)

        if not characters:
            message = (
                "There are no characters other than the player in your playthrough."
            )
            return render_template("participants.html", characters=[], message=message)
        return render_template("participants.html", characters=characters)

    def post(self):
        selected_characters = request.form.getlist("selected_characters")
        purpose = request.form.get("purpose", "")
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        if len(selected_characters) < 1:
            error = "Please select at least one character."

            return render_template(
                "participants.html",
                characters=self._get_possible_characters_for_chat(playthrough_name),
                error=error,
            )
        session["participants"] = selected_characters
        session["purpose"] = purpose

        logger.info("Purpose stored in session: %s", session.get("purpose"))

        session.pop("place_description", None)
        return redirect(url_for("chat"))
