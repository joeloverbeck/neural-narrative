from flask import Flask

from src.views.character_generation_view import CharacterGenerationView
from src.views.character_memories_view import CharacterMemoriesView
from src.views.chat_view import ChatView
from src.views.index_view import IndexView
from src.views.location_hub_view import LocationHubView
from src.views.participants_view import ParticipantsView
from src.views.travel_view import TravelView

app = Flask(__name__)

app.secret_key = b"neural-narrative"

# Register the view
app.add_url_rule("/", view_func=IndexView.as_view("index"))
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

if __name__ == "__main__":
    app.run(debug=True)
