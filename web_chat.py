import logging.config

from flask import Flask, request, jsonify

from src.filesystem.filesystem_manager import FilesystemManager
from src.services.voices_services import VoicesServices
from src.views.character_generation_view import CharacterGenerationView
from src.views.character_memories_view import CharacterMemoriesView
from src.views.character_voice_view import CharacterVoiceView
from src.views.characters_hub_view import CharactersHubView
from src.views.chat_view import ChatView
from src.views.goal_resolution_view import GoalResolutionView
from src.views.index_view import IndexView
from src.views.location_hub_view import LocationHubView
from src.views.participants_view import ParticipantsView
from src.views.story_hub_view import StoryHubView
from src.views.travel_view import TravelView

logging.config.dictConfig(FilesystemManager().get_logging_config_file())

app = Flask(__name__)

app.secret_key = b"neural-narrative"

# Register the view
app.add_url_rule("/", view_func=IndexView.as_view("index"))
app.add_url_rule("/story-hub", view_func=StoryHubView.as_view("story-hub"))
app.add_url_rule(
    "/characters-hub", view_func=CharactersHubView.as_view("characters-hub")
)
app.add_url_rule("/location-hub", view_func=LocationHubView.as_view("location-hub"))
app.add_url_rule("/travel", view_func=TravelView.as_view("travel"))
app.add_url_rule("/participants", view_func=ParticipantsView.as_view("participants"))
app.add_url_rule("/chat", view_func=ChatView.as_view("chat"))
app.add_url_rule(
    "/character-generation",
    view_func=CharacterGenerationView.as_view("character-generation"),
)
app.add_url_rule(
    "/character-memories",
    view_func=CharacterMemoriesView.as_view("character-memories"),
    methods=["GET", "POST"],
)
app.add_url_rule(
    "/character-voice", view_func=CharacterVoiceView.as_view("character-voice")
)
app.add_url_rule(
    "/goal-resolution", view_func=GoalResolutionView.as_view("goal-resolution")
)


@app.route("/play-audio", methods=["POST"])
def play_audio_route():
    data = request.get_json()
    file_path = data.get("file_path")

    VoicesServices().play_voice_line(file_path)

    # Return a JSON response without waiting for the audio to finish
    return jsonify({"message": "Audio playback started"}), 200


if __name__ == "__main__":
    app.run(debug=True)
