from flask import redirect, url_for, session, render_template, request
from flask.views import MethodView

from src.base.constants import TIME_ADVANCED_DUE_TO_TRAVELING
from src.base.playthrough_manager import PlaythroughManager
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.movements.models.travel_narration import TravelNarration
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.enums import LlmClientType
from src.prompting.factories.travel_narration_factory import TravelNarrationFactory
from src.prompting.llms import Llms
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

        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                LlmClientType.INSTRUCTOR, Llms().for_travel_narration(), TravelNarration
            ).compose_factory()
        )
        player_data_for_prompt_factory = PlayerDataForPromptFactory(
            playthrough_name, CharacterFactory(playthrough_name)
        )
        party_data_for_prompt_factory = PartyDataForPromptFactory(
            playthrough_name, player_data_for_prompt_factory
        )
        player_and_followers_information_factory = PlayerAndFollowersInformationFactory(
            party_data_for_prompt_factory
        )
        map_manager_factory = MapManagerFactory(playthrough_name)
        product = TravelNarrationFactory(
            playthrough_name,
            destination_identifier,
            produce_tool_response_strategy_factory,
            player_and_followers_information_factory,
            map_manager_factory,
        ).generate_product()
        if not product.is_valid():
            return redirect(url_for("location-hub"))
        travel_narration = product.get()
        PlaythroughManager(playthrough_name).add_to_adventure(travel_narration + "\n")
        destination_place_data = (
            MapManagerFactory(playthrough_name)
            .create_map_manager()
            .get_place_full_data(destination_identifier)
        )
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
        TimeManager(playthrough_name).advance_time(TIME_ADVANCED_DUE_TO_TRAVELING)
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
