from flask import redirect, url_for, session, render_template, request
from flask.views import MethodView

from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)
from src.config.config_manager import ConfigManager
from src.constants import (
    TIME_ADVANCED_DUE_TO_TRAVELING,
)
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.factories.travel_narration_factory import TravelNarrationFactory
from src.services.place_service import PlaceService
from src.services.web_service import WebService
from src.time.time_manager import TimeManager


class TravelView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        destination_identifier = session.get("destination_identifier")
        if not destination_identifier:
            return redirect(url_for("location-hub"))

        produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
            OpenRouterLlmClientFactory().create_llm_client(),
            ConfigManager().get_heavy_llm(),
        )

        player_data_for_prompt_factory = PlayerDataForPromptFactory(playthrough_name)

        party_data_for_prompt_factory = PartyDataForPromptFactory(
            playthrough_name, player_data_for_prompt_factory
        )

        product = TravelNarrationFactory(
            playthrough_name,
            destination_identifier,
            produce_tool_response_strategy_factory,
            party_data_for_prompt_factory,
        ).generate_product()

        if not product.is_valid():
            return redirect(url_for("location-hub"))

        travel_narration = product.get()

        # Add the travel narration to the adventure.
        PlaythroughManager(playthrough_name).add_to_adventure(travel_narration + "\n")

        destination_place_data = MapManager(playthrough_name).get_place_full_data(
            destination_identifier
        )

        # Remove the dialogue in the session, lest the travel narration not fit.
        session.pop("dialogue", None)

        return render_template(
            "travel.html",
            travel_narration=travel_narration,
            destination_name=destination_place_data["area_data"]["name"],
            destination_identifier=destination_identifier,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        action = request.form.get("action")
        if not action:
            return redirect(url_for("location-hub"))

        # Advance time significantly
        TimeManager(playthrough_name).advance_time(TIME_ADVANCED_DUE_TO_TRAVELING)

        # Dispatch to the appropriate handler method
        method_name = WebService.create_method_name(action)
        method = getattr(self, method_name, None)

        if method:
            return method(playthrough_name)
        else:
            return redirect(url_for("location-hub"))

    @staticmethod
    def handle_enter_area(playthrough_name):
        destination_identifier = request.form.get("destination_identifier")

        PlaceService().visit_location(playthrough_name, destination_identifier)

        return redirect(url_for("location-hub"))
