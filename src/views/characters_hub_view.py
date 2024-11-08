from flask import session, redirect, url_for, render_template, flash, request
from flask.views import MethodView

from src.base.commands.change_protagonist_command import ChangeProtagonistCommand
from src.base.configs.change_protagonist_command_config import (
    ChangeProtagonistCommandConfig,
)
from src.base.configs.change_protagonist_command_factories_config import (
    ChangeProtagonistCommandFactoriesConfig,
)
from src.base.factories.remove_followers_command_factory import (
    RemoveFollowersCommandFactory,
)
from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.maps.factories.get_place_identifier_of_character_location_algorithm_factory import (
    GetPlaceIdentifierOfCharacterLocationAlgorithmFactory,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.factories.remove_character_from_place_command_factory import (
    RemoveCharacterFromPlaceCommandFactory,
)
from src.movements.factories.place_character_at_place_command_factory import (
    PlaceCharacterAtPlaceCommandFactory,
)


class CharactersHubView(MethodView):

    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        player_character = Character(
            playthrough_name,
            PlaythroughManager(playthrough_name).get_player_identifier(),
        )

        characters_manager = CharactersManager(playthrough_name)
        all_characters = characters_manager.get_all_characters()

        return render_template(
            "characters-hub.html",
            player_character=player_character,
            all_characters=all_characters,
        )

    @staticmethod
    def post():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        new_protagonist_identifier = request.form.get("new_protagonist_identifier")

        if not new_protagonist_identifier:
            flash("No protagonist selected.", "error")
            return redirect(url_for("characters-hub"))

        place_character_at_place_command_factory = PlaceCharacterAtPlaceCommandFactory(
            playthrough_name
        )
        remove_followers_command_factory = RemoveFollowersCommandFactory(
            playthrough_name, place_character_at_place_command_factory
        )

        get_place_identifier_of_character_location_algorithm_factory = (
            GetPlaceIdentifierOfCharacterLocationAlgorithmFactory(playthrough_name)
        )

        place_manager_factory = PlaceManagerFactory(playthrough_name)

        remove_character_from_place_command_factory = (
            RemoveCharacterFromPlaceCommandFactory(
                playthrough_name, place_manager_factory
            )
        )

        try:
            ChangeProtagonistCommand(
                ChangeProtagonistCommandConfig(
                    playthrough_name, new_protagonist_identifier
                ),
                ChangeProtagonistCommandFactoriesConfig(
                    place_character_at_place_command_factory,
                    remove_followers_command_factory,
                    get_place_identifier_of_character_location_algorithm_factory,
                    remove_character_from_place_command_factory,
                ),
            ).execute()
        except Exception as e:
            flash(f"Failed to change the protagonist: {str(e)}", "error")
            return redirect(url_for("characters-hub"))

        flash("Protagonist changed successfully.", "success")
        return redirect(url_for("characters-hub"))
