# views/characters_hub_view.py
from flask import session, redirect, url_for, render_template
from flask.views import MethodView

from src.characters.characters_manager import CharactersManager
from src.playthrough_manager import PlaythroughManager
from src.services.web_service import WebService


class CharactersHubView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")

        if not playthrough_name:
            return redirect(url_for("index"))

        characters_manager = CharactersManager(playthrough_name)

        # Get the player's character
        player_character = characters_manager.load_character_data(
            PlaythroughManager(playthrough_name).get_player_identifier()
        )

        # Format image URL
        player_character["image_url"] = WebService.format_image_url_of_character(
            player_character
        )

        return render_template("characters-hub.html", player_character=player_character)
