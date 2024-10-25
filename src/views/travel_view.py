import threading

from flask import redirect, url_for, session, render_template, request, jsonify
from flask.views import MethodView

from src.base.constants import TIME_ADVANCED_DUE_TO_TRAVELING, NARRATOR_VOICE_MODEL
from src.base.playthrough_manager import PlaythroughManager
from src.characters.composers.player_and_followers_information_factory_composer import (
    PlayerAndFollowersInformationFactoryComposer,
)
from src.characters.factories.character_factory import CharacterFactory
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.movements.configs.travel_narration_factory_config import (
    TravelNarrationFactoryConfig,
)
from src.movements.configs.travel_narration_factory_factories_config import (
    TravelNarrationFactoryFactoriesConfig,
)
from src.movements.factories.travel_narration_factory import TravelNarrationFactory
from src.movements.models.travel import Travel
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms
from src.services.place_service import PlaceService
from src.time.time_manager import TimeManager
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)


class TravelView(MethodView):

    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        destination_identifier = session.get("destination_identifier")
        if not destination_identifier:
            return redirect(url_for("location-hub"))

        # Get current location (origin area)
        current_area_identifier = PlaythroughManager(
            playthrough_name
        ).get_current_place_identifier()

        # Get the names of origin and destination areas
        map_manager = MapManagerFactory(playthrough_name).create_map_manager()
        current_area_data = map_manager.get_place_full_data(current_area_identifier)
        destination_area_data = map_manager.get_place_full_data(destination_identifier)

        origin_area_name = current_area_data["area_data"]["name"]
        destination_area_name = destination_area_data["area_data"]["name"]

        # Get current time of day
        current_time = TimeManager(playthrough_name).get_time_of_the_day()

        return render_template(
            "travel.html",
            destination_identifier=destination_identifier,
            origin_area_name=origin_area_name,
            destination_area_name=destination_area_name,
            current_time=current_time,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            # Handle AJAX request
            action = request.form.get("submit_action")
            if action == "travel":
                TimeManager(playthrough_name).advance_time(
                    TIME_ADVANCED_DUE_TO_TRAVELING
                )
                return self.handle_travel(playthrough_name)
            else:
                return jsonify({"success": False, "error": "Invalid action"})
        else:
            # Handle normal POST request (Enter area)
            action = request.form.get("submit_action")
            if action == "enter_area":
                return self.handle_enter_area(playthrough_name)
            else:
                return redirect(url_for("location-hub"))

    @staticmethod
    def handle_travel(playthrough_name):
        destination_identifier = session.get("destination_identifier")
        if not destination_identifier:
            return jsonify({"success": False, "error": "No destination specified"})

        # The page should have sent the "travel_context" variable, that includes
        # the context introduced or not by the player in a textbox over the Travel button.
        travel_context = request.form.get("travel_context", "")

        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                Llms().for_travel_narration()
            ).compose_factory()
        )

        player_and_followers_information_factory = (
            PlayerAndFollowersInformationFactoryComposer(
                playthrough_name
            ).compose_factory()
        )

        map_manager_factory = MapManagerFactory(playthrough_name)

        character_factory = CharacterFactory(playthrough_name)

        product = TravelNarrationFactory(
            TravelNarrationFactoryConfig(
                playthrough_name, destination_identifier, travel_context
            ),
            TravelNarrationFactoryFactoriesConfig(
                produce_tool_response_strategy_factory,
                player_and_followers_information_factory,
                character_factory,
                map_manager_factory,
            ),
        ).generate_product(Travel)

        if not product.is_valid():
            return jsonify(
                {"success": False, "error": "Failed to generate travel narration"}
            )

        narrative = product.get_narrative()
        outcome = product.get_outcome()

        PlaythroughManager(playthrough_name).add_to_adventure(
            narrative + "\n" + outcome
        )

        destination_place_data = (
            MapManagerFactory(playthrough_name)
            .create_map_manager()
            .get_place_full_data(destination_identifier)
        )

        destination_area_name = destination_place_data["area_data"]["name"]

        # Generate voice lines in parallel using threading
        direct_voice_line_generation_algorithm_factory = (
            DirectVoiceLineGenerationAlgorithmFactory
        )

        result_dict = {}

        def generate_narrative_voice_line():
            result_dict["narrative_voice_line_url"] = (
                direct_voice_line_generation_algorithm_factory.create_algorithm(
                    "narrator", product.get_narrative(), NARRATOR_VOICE_MODEL
                ).direct_voice_line_generation()
            )

        def generate_outcome_voice_line():
            result_dict["outcome_voice_line_url"] = (
                direct_voice_line_generation_algorithm_factory.create_algorithm(
                    "narrator", product.get_outcome(), NARRATOR_VOICE_MODEL
                ).direct_voice_line_generation()
            )

        threads = []

        t1 = threading.Thread(target=generate_narrative_voice_line)
        t2 = threading.Thread(target=generate_outcome_voice_line)
        threads.append(t1)
        threads.append(t2)
        t1.start()
        t2.start()

        for t in threads:
            t.join()

        narrative_voice_line_url = result_dict.get("narrative_voice_line_url")
        outcome_voice_line_url = result_dict.get("outcome_voice_line_url")

        return jsonify(
            {
                "success": True,
                "narrative": narrative,
                "outcome": outcome,
                "narrative_voice_line_url": narrative_voice_line_url,
                "outcome_voice_line_url": outcome_voice_line_url,
                "destination_name": destination_area_name,
                "destination_identifier": destination_identifier,
                "enter_area_url": url_for(
                    "travel"
                ),  # Include the URL for entering the area
            }
        )

    @staticmethod
    def handle_enter_area(playthrough_name):
        destination_identifier = request.form.get("destination_identifier")

        PlaceService().visit_location(playthrough_name, destination_identifier)

        return redirect(url_for("location-hub"))
