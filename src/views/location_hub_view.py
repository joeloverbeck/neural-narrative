from typing import List

from flask import session, redirect, url_for, render_template, request
from flask.views import MethodView

from src.characters.characters_manager import CharactersManager
from src.maps.map_manager import MapManager
from src.movements.movement_manager import MovementManager
from src.playthrough_manager import PlaythroughManager
from src.services.web_service import WebService


class LocationHubView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")

        if not playthrough_name:
            return redirect(url_for("index"))

        # Get the current place template (a string) of the current location,
        # so that it can be shown in the web page.
        current_place = MapManager(playthrough_name).get_current_place_template()

        # Retrieve the current characters present at the location but
        # that aren't members of the player's party (his followers).
        characters_manager = CharactersManager(playthrough_name)

        # Let's retrieve the data of the characters at the current place.
        # Each entry has a "name" attribute.
        characters_at_current_place: List[dict] = (
            characters_manager.get_characters_at_current_place()
        )

        WebService.format_image_urls_of_characters(characters_at_current_place)

        # Let's retrieve the data of the player's followers.
        # Each entry has a "name" attribute.
        followers: List[dict] = characters_manager.get_followers()

        WebService.format_image_urls_of_characters(followers)

        return render_template(
            "location-hub.html",
            current_place=current_place,
            characters=characters_at_current_place,
            followers=followers,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")

        if not playthrough_name:
            return redirect(url_for("index"))

        movement_manager = MovementManager(playthrough_name)
        playthrough_manager = PlaythroughManager(playthrough_name)

        # Determine which action was taken
        action = request.form.get("action")

        if action == "Add to Followers":
            # Add selected characters to followers
            selected_add = request.form.getlist("add_followers")

            for character_id in selected_add:
                movement_manager.add_follower(
                    character_id, playthrough_manager.get_current_place_identifier()
                )
        elif action == "Remove from Followers":
            # Remove selected followers
            selected_remove = request.form.getlist("remove_followers")
            for follower_id in selected_remove:
                movement_manager.remove_follower(
                    follower_id, playthrough_manager.get_current_place_identifier()
                )

        return redirect(url_for("location-hub"))
