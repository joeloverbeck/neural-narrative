# views/character_edit_view.py

from flask import session, redirect, url_for, render_template, request, flash
from flask.views import MethodView

from src.characters.character import Character
from src.characters.characters_manager import CharactersManager


class CharacterEditView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        characters_manager = CharactersManager(playthrough_name)
        all_characters = characters_manager.get_all_characters()
        selected_character_identifier = request.args.get("character_identifier")
        selected_character = None
        character_data = {}

        if selected_character_identifier:
            selected_character = Character(
                playthrough_name, selected_character_identifier
            )
            character_data = {
                "description": selected_character.description,
                "profile": selected_character.profile,
                "health": selected_character.health,
                "equipment": selected_character.equipment,
            }

        for character in all_characters:
            character["selected"] = False
            if (
                selected_character
                and character["identifier"] == selected_character.identifier
            ):
                character["selected"] = True

        return render_template(
            "character-edit.html",
            all_characters=all_characters,
            selected_character=selected_character,
            character_data=character_data,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        character_identifier = request.form.get("character_identifier")
        if character_identifier:
            selected_character = Character(playthrough_name, character_identifier)
            description = request.form.get("description", "")
            profile = request.form.get("profile", "")
            health = request.form.get("health", "")
            equipment = request.form.get("equipment", "")

            selected_character.update_data(
                {
                    "description": description,
                    "profile": profile,
                    "health": health,
                    "equipment": equipment,
                }
            )

            selected_character.save()

            flash("Character data saved successfully.", "success")
            return redirect(
                url_for("character-edit", character_identifier=character_identifier)
            )
        else:
            flash("No character selected.", "error")
            return redirect(url_for("character-edit"))
