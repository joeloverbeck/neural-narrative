import logging.config

from flask import Flask

from src.base.constants import (
    RESEARCH_RESOLUTION_GENERATION_PROMPT_FILE,
    INVESTIGATE_RESOLUTION_GENERATION_PROMPT_FILE,
    GATHER_SUPPLIES_RESOLUTION_GENERATION_PROMPT_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.views.action_view import action_view
from src.views.actions_view import ActionsView
from src.views.character_generation_view import CharacterGenerationView
from src.views.character_memories_view import CharacterMemoriesView
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

logging.config.dictConfig(FilesystemManager().get_logging_config_file())
app = Flask(__name__)
app.secret_key = b"neural-narrative"
logger = logging.getLogger(__name__)
app.add_url_rule("/", view_func=IndexView.as_view("index"))
app.add_url_rule("/places", view_func=PlacesView.as_view("places"))
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
    "/character-secrets", view_func=CharacterSecretsView.as_view("character-secrets")
)
app.add_url_rule("/actions", view_func=ActionsView.as_view("actions"))
app.add_url_rule("/connections", view_func=ConnectionsView.as_view("connections"))


@app.route("/research", methods=["GET", "POST"])
def research():
    return action_view(
        action_name="Research",
        action_icon="fa-book",
        action_endpoint="research",
        prompt_file=RESEARCH_RESOLUTION_GENERATION_PROMPT_FILE,
    )


@app.route("/investigate", methods=["GET", "POST"])
def investigate():
    return action_view(
        action_name="Investigate",
        action_icon="fa-search",
        action_endpoint="investigate",
        prompt_file=INVESTIGATE_RESOLUTION_GENERATION_PROMPT_FILE,
    )


@app.route("/gather_supplies", methods=["GET", "POST"])
def gather_supplies():
    return action_view(
        action_name="Gather Supplies",
        action_icon="fa-clipboard-list",
        action_endpoint="gather_supplies",
        prompt_file=GATHER_SUPPLIES_RESOLUTION_GENERATION_PROMPT_FILE,
    )


if __name__ == "__main__":
    app.run(debug=True)
