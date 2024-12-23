# views/character_edit_view.py

from flask import session, redirect, url_for, render_template, request, flash
from flask.views import MethodView

from src.characters.character import Character
from src.characters.characters_manager import CharactersManager


class CharacterEditView(MethodView):
    @staticmethod
    def get():
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
                "personality": selected_character.personality,
                "profile": selected_character.profile,
                "likes": selected_character.likes,
                "dislikes": selected_character.dislikes,
                "speech_patterns": selected_character.speech_patterns,
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

    @staticmethod
    def post():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        character_identifier = request.form.get("character_identifier")
        if character_identifier:
            selected_character = Character(playthrough_name, character_identifier)
            description = request.form.get("description", "")
            personality = request.form.get("personality", "")
            profile = request.form.get("profile", "")
            likes = request.form.get("likes", "")
            dislikes = request.form.get("dislikes", "")
            speech_patterns = request.form.get("speech_patterns", "")
            health = request.form.get("health", "")
            equipment = request.form.get("equipment", "")

            selected_character.update_data(
                {
                    "description": description,
                    "personality": personality,
                    "profile": profile,
                    "likes": likes,
                    "dislikes": dislikes,
                    "speech_patterns": speech_patterns,
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
