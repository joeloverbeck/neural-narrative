from flask import session, redirect, url_for, render_template, request
from flask.views import MethodView

from src.characters.characters_manager import CharactersManager
from src.filesystem.filesystem_manager import FilesystemManager
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
            # Load the selected character's data
            selected_character = characters_manager.load_character_data(
                selected_character_identifier
            )
            # Get the assigned voice model
            selected_voice_model = selected_character.get("voice_model", "")

        for character in all_characters:
            character["selected"] = False
            if (
                selected_character
                and character["identifier"] == selected_character["identifier"]
            ):
                character["selected"] = True

        voice_manager = VoiceManager()

        all_tags = voice_manager.get_all_tags()

        # If tags are selected, filter voice models
        if selected_tags:
            voice_models = voice_manager.filter_voice_models_by_tags(selected_tags)
        else:
            voice_models = {}  # No voice models to display initially

        # Define categories and their tags
        categories_tags = {
            "voice_gender": ["MALE", "FEMALE"],
            "voice_age": [
                "CHILDLIKE",
                "TEENAGE",
                "YOUNG ADULT",
                "ADULT",
                "MIDDLE-AGED",
                "ELDERLY",
            ],
            "voice_emotion": [
                "CALM",
                "HAPPY",
                "SAD",
                "ANGRY",
                "MENACING",
                "NERVOUS",
                "MELANCHOLIC",
                "JOYFUL",
                "CONFIDENT",
                "ARROGANT",
                "ANXIOUS",
                "AGGRESSIVE",
                "HOPEFUL",
                "STOIC",
                "FRIGHTENED",
                "SURPRISED",
                "PLAYFUL",
                "EXCITED",
                "RESIGNED",
            ],
            "voice_tempo": [
                "FAST-PACED",
                "SLOW",
                "STEADY",
                "DRAWLING",
                "RAPID-FIRE",
            ],
            "voice_volume": [
                "WHISPERING",
                "SOFT-SPOKEN",
                "LOUD",
                "BOOMING",
                "QUIET",
            ],
            "voice_texture": [
                "GRAVELLY",
                "SMOOTH",
                "RASPY",
                "NASAL",
                "CRISP",
                "MUFFLED",
                "ETHEREAL",
                "WHISPERY",
                "CLEAR",
                "BREATHLESS",
                "HOARSE",
                "WARM",
                "COLD",
                "METALLIC",
                "MECHANICAL",
                "AIRY",
                "GUTTURAL",
            ],
            "voice_style": [
                "FORMAL",
                "CASUAL",
                "INTENSE",
                "DRAMATIC",
                "MONOTONE",
                "FLIRTATIOUS",
                "SARCASTIC",
                "HUMOROUS",
                "MELODIC",
                "AUTHORITATIVE",
                "NARRATIVE",
                "INSTRUCTIONAL",
            ],
            "voice_personality": [
                "INNOCENT",
                "YOUTHFUL",
                "SULTRY",
                "HEROIC",
                "VILLAINOUS",
                "NOBLE",
                "MYSTERIOUS",
                "SLY",
                "CHARMING",
                "ENERGETIC",
                "WITTY",
                "CYNICAL",
                "KIND",
                "CALCULATING",
                "WISE",
                "ENTHUSIASTIC",
                "MANIPULATIVE",
                "ECCENTRIC",
                "PHILOSOPHICAL",
                "ADVENTUROUS",
                "SKEPTICAL",
                "BRAVE",
                "SCHEMING",
                "NAIVE",
                "OPTIMISTIC",
                "PESSIMISTIC",
                "PARANOID",
            ],
            "voice_special_effects": [
                "NO SPECIAL EFFECTS",
                "ROBOTIC",
                "ALIEN",
                "DEMON-LIKE",
                "MAGICAL",
                "DISTORTED",
                "ECHOED",
                "GHOSTLY",
                "FUTURISTIC",
                "RETRO",
                "SYNTHESIZED",
            ],
        }

        return render_template(
            "character-voice.html",
            all_characters=all_characters,
            selected_character=selected_character,
            selected_voice_model=selected_voice_model,
            voice_models=voice_models,
            selected_tags=selected_tags,
            all_tags=all_tags,
            categories_tags=categories_tags,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        character_identifier = request.form.get("character_identifier")
        new_voice_model = request.form.get("voice_model")

        print(f"Will assign voice model: {new_voice_model} to {character_identifier}")

        if character_identifier and new_voice_model:
            # Load character data
            filesystem_manager = FilesystemManager()

            characters_file = filesystem_manager.load_existing_or_new_json_file(
                filesystem_manager.get_file_path_to_characters_file(playthrough_name)
            )

            characters_file[character_identifier]["voice_model"] = new_voice_model

            filesystem_manager.save_json_file(
                characters_file,
                filesystem_manager.get_file_path_to_characters_file(playthrough_name),
            )

            # Add a success message to the session
            session["voice_model_changed_message"] = "Voice model updated successfully."

        return redirect(
            url_for("character-voice", character_identifier=character_identifier)
        )
