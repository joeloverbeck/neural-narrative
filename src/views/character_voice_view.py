from flask import session, redirect, url_for, render_template, request, flash
from flask.views import MethodView

from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.voices.algorithms.match_voice_data_to_voice_model_algorithm import (
    MatchVoiceDataToVoiceModelAlgorithm,
)
from src.voices.enums import (
    voice_categories_tags,
)
from src.voices.voice_attributes import VoiceAttributes
from src.voices.voice_manager import VoiceManager


class CharacterVoiceView(MethodView):

    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        characters_manager = CharactersManager(playthrough_name)
        all_characters = characters_manager.get_all_characters()
        selected_character_identifier = request.args.get("character_identifier")
        selected_tags = request.args.getlist("tags")
        selected_voice_model = None
        selected_character = None
        if selected_character_identifier:
            selected_character = Character(
                playthrough_name, selected_character_identifier
            )
            selected_voice_model = selected_character.voice_model
        for character in all_characters:
            character["selected"] = False
            if (
                selected_character
                and character["identifier"] == selected_character.identifier
            ):
                character["selected"] = True
        voice_manager = VoiceManager()
        all_tags = voice_manager.get_all_tags()
        if selected_tags:
            voice_models = voice_manager.filter_voice_models_by_tags(selected_tags)
        else:
            voice_models = {}

        return render_template(
            "character-voice.html",
            all_characters=all_characters,
            selected_character=selected_character,
            selected_voice_model=selected_voice_model,
            voice_models=voice_models,
            selected_tags=selected_tags,
            all_tags=all_tags,
            categories_tags=voice_categories_tags,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        if "match_voice_model" in request.form:
            character_identifier = request.form.get("character_identifier")
            if not character_identifier:
                flash("Character identifier is missing.", "error")
                return redirect(url_for("character-voice"))
            try:
                character = Character(playthrough_name, character_identifier)
                matched_voice_model = MatchVoiceDataToVoiceModelAlgorithm.match(
                    VoiceAttributes(
                        character.voice_gender,
                        character.voice_age,
                        character.voice_emotion,
                        character.voice_tempo,
                        character.voice_volume,
                        character.voice_texture,
                        character.voice_tone,
                        character.voice_style,
                        character.personality,
                        character.voice_special_effects,
                    )
                )
                character = Character(playthrough_name, character_identifier)
                character.update_data({"voice_model": matched_voice_model})
                character.save()
                session["voice_model_changed_message"] = (
                    f"Voice model '{matched_voice_model}' matched and assigned successfully."
                )
            except KeyError as e:
                flash(f"Error: {str(e)}", "error")
            except ValueError as e:
                flash(f"Error: {str(e)}", "error")
            except Exception as e:
                flash(f"An unexpected error occurred: {str(e)}", "error")
            return redirect(
                url_for("character-voice", character_identifier=character_identifier)
            )
        elif "voice_model" in request.form:
            character_identifier = request.form.get("character_identifier")
            new_voice_model = request.form.get("voice_model")
            if character_identifier and new_voice_model:
                try:
                    character = Character(playthrough_name, character_identifier)
                    character.update_data({"voice_model": new_voice_model})
                    character.save()
                    session["voice_model_changed_message"] = (
                        "Voice model updated successfully."
                    )
                except KeyError as e:
                    flash(f"Error: {str(e)}", "error")
                except ValueError as e:
                    flash(f"Error: {str(e)}", "error")
                except Exception as e:
                    flash(f"An unexpected error occurred: {str(e)}", "error")
                return redirect(
                    url_for(
                        "character-voice", character_identifier=character_identifier
                    )
                )
            else:
                flash("Character identifier or voice model is missing.", "error")
                return redirect(url_for("character-voice"))
        else:
            flash("Invalid form submission.", "error")
            return redirect(url_for("character-voice"))
