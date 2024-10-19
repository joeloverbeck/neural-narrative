# views/characters_hub_view.py
from flask import session, redirect, url_for, render_template
from flask.views import MethodView

from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character


class CharactersHubView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")

        if not playthrough_name:
            return redirect(url_for("index"))

        # Get the player's character
        player_character = Character(
            playthrough_name,
            PlaythroughManager(playthrough_name).get_player_identifier(),
        )

        return render_template("characters-hub.html", player_character=player_character)
