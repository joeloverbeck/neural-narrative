# views/character_purpose_view.py
from flask import session, redirect, url_for, render_template, request, flash
from flask.views import MethodView

from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.characters.factories.character_factory import CharacterFactory
from src.filesystem.file_operations import (
    create_empty_file_if_not_exists,
    read_file,
    write_file,
)
from src.filesystem.path_manager import PathManager
from src.interfaces.web_interface_manager import WebInterfaceManager


class CharacterPurposeView(MethodView):

    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        characters_manager = CharactersManager(playthrough_name)
        all_characters = characters_manager.get_all_characters()
        selected_character_identifier = request.args.get("character_identifier")
        character_purpose = ""
        selected_character = None

        if selected_character_identifier:
            selected_character = Character(
                playthrough_name, selected_character_identifier
            )
            path_manager = PathManager()
            purpose_path = path_manager.get_purpose_path(
                playthrough_name, selected_character_identifier, selected_character.name
            )
            create_empty_file_if_not_exists(purpose_path)
            character_purpose = read_file(purpose_path)

        for character in all_characters:
            character["selected"] = False
            if (
                selected_character
                and character["identifier"] == selected_character.identifier
            ):
                character["selected"] = True

        return render_template(
            "character-purpose.html",
            all_characters=all_characters,
            selected_character=selected_character,
            character_purpose=character_purpose,
        )

    @staticmethod
    def post():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        action = request.form.get("submit_action")
        character_identifier = request.form.get("character_identifier")

        character = CharacterFactory(playthrough_name).create_character(
            character_identifier
        )

        if action == "save_purpose" and character_identifier:
            new_purpose = request.form.get("character_purpose", "")
            new_purpose = WebInterfaceManager.remove_excessive_newline_characters(
                new_purpose
            )
            selected_character = Character(playthrough_name, character_identifier)
            path_manager = PathManager()
            purpose_path = path_manager.get_purpose_path(
                playthrough_name, character_identifier, selected_character.name
            )
            write_file(purpose_path, new_purpose)
            flash(f"{character.name}'s purpose saved.", "success")

        return redirect(
            url_for("character-purpose", character_identifier=character_identifier)
        )
