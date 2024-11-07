import logging.config
import re

from flask import Flask
from markupsafe import Markup
from waitress import serve

from src.filesystem.file_operations import read_json_file
from src.filesystem.path_manager import PathManager
from src.views.action_view import action_view
from src.views.actions_view import ActionsView
from src.views.add_participants_view import AddParticipantsView
from src.views.attach_places_view import AttachPlacesView
from src.views.character_edit_view import CharacterEditView
from src.views.character_generation_view import CharacterGenerationView
from src.views.character_memories_view import CharacterMemoriesView
from src.views.character_purpose_view import CharacterPurposeView
from src.views.character_secrets_view import CharacterSecretsView
from src.views.character_voice_view import CharacterVoiceView
from src.views.characters_hub_view import CharactersHubView
from src.views.chat_view import ChatView
from src.views.connections_view import ConnectionsView
from src.views.index_view import IndexView
from src.views.location_hub_view import LocationHubView
from src.views.participants_view import ParticipantsView
from src.views.places_view import PlacesView
from src.views.story_hub_view import StoryHubView
from src.views.travel_view import TravelView
from src.views.writers_room_view import WritersRoomView

logging.config.dictConfig(read_json_file(PathManager().get_logging_config()))

app = Flask(__name__)
app.secret_key = b"neural-narrative"


def bold_text(text):
    """
    Convert **text** to <strong>text</strong> for bold formatting.
    """
    # Regular expression to find **text**
    pattern = r"\*\*(.*?)\*\*"
    # Replace with <strong>text</strong>
    replaced_text = re.sub(pattern, r"<strong>\1</strong>", text)
    return Markup(replaced_text)


# Register the custom filter
app.jinja_env.filters["bold_text"] = bold_text

logger = logging.getLogger(__name__)

app.add_url_rule("/", view_func=IndexView.as_view("index"))
app.add_url_rule("/places", view_func=PlacesView.as_view("places"))
app.add_url_rule("/story-hub", view_func=StoryHubView.as_view("story-hub"))
app.add_url_rule("/writers-room", view_func=WritersRoomView.as_view("writers-room"))
app.add_url_rule(
    "/characters-hub", view_func=CharactersHubView.as_view("characters-hub")
)
app.add_url_rule("/location-hub", view_func=LocationHubView.as_view("location-hub"))
app.add_url_rule("/attach-places", view_func=AttachPlacesView.as_view("attach-places"))
app.add_url_rule("/travel", view_func=TravelView.as_view("travel"))
app.add_url_rule("/participants", view_func=ParticipantsView.as_view("participants"))
app.add_url_rule("/chat", view_func=ChatView.as_view("chat"))
app.add_url_rule(
    "/add_participants", view_func=AddParticipantsView.as_view("add_participants")
)
app.add_url_rule(
    "/character-generation",
    view_func=CharacterGenerationView.as_view("character-generation"),
)
app.add_url_rule(
    "/character-edit", view_func=CharacterEditView.as_view("character-edit")
)
app.add_url_rule(
    "/character-memories",
    view_func=CharacterMemoriesView.as_view("character-memories"),
    methods=["GET", "POST"],
)
app.add_url_rule(
    "/character-purpose", view_func=CharacterPurposeView.as_view("character-purpose")
)
app.add_url_rule(
    "/character-voice", view_func=CharacterVoiceView.as_view("character-voice")
)
app.add_url_rule(
    "/character-secrets", view_func=CharacterSecretsView.as_view("character-secrets")
)
app.add_url_rule("/actions", view_func=ActionsView.as_view("actions"))
app.add_url_rule("/connections", view_func=ConnectionsView.as_view("connections"))


@app.route("/research", methods=["GET", "POST"])
def research():
    path_manager = PathManager()

    return action_view(
        action_name="Research",
        action_icon="fa-book",
        action_endpoint="research",
        prompt_file=path_manager.get_research_resolution_generation_prompt_path(),
    )


@app.route("/investigate", methods=["GET", "POST"])
def investigate():
    path_manager = PathManager()

    return action_view(
        action_name="Investigate",
        action_icon="fa-search",
        action_endpoint="investigate",
        prompt_file=path_manager.get_investigate_resolution_generation_prompt_path(),
    )


@app.route("/gather_supplies", methods=["GET", "POST"])
def gather_supplies():
    path_manager = PathManager()

    return action_view(
        action_name="Gather Supplies",
        action_icon="fa-clipboard-list",
        action_endpoint="gather_supplies",
        prompt_file=path_manager.get_gather_supplies_resolution_generation_prompt_path(),
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
