from pathlib import Path

from flask import redirect, url_for, session, render_template, request, jsonify
from flask.views import MethodView

from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character
from src.characters.composers.relevant_characters_information_factory_composer import (
    RelevantCharactersInformationFactoryComposer,
)
from src.characters.factories.character_factory import CharacterFactory
from src.characters.strategies.followers_identifiers_strategy import (
    FollowersIdentifiersStrategy,
)
from src.filesystem.config_loader import ConfigLoader
from src.maps.algorithms.get_place_full_data_algorithm import GetPlaceFullDataAlgorithm
from src.maps.factories.get_place_full_data_algorithm_factory import (
    GetPlaceFullDataAlgorithmFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
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
from src.services.web_service import WebService
from src.time.time_manager import TimeManager
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)


class TravelView(MethodView):

    @staticmethod
    def get():
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
        place_manager_factory = PlaceManagerFactory(playthrough_name)
        hierarchy_manager_factory = HierarchyManagerFactory(playthrough_name)
        get_place_full_data_algorithm_factory = GetPlaceFullDataAlgorithmFactory(
            place_manager_factory, hierarchy_manager_factory
        )
        current_area_data = get_place_full_data_algorithm_factory.create_algorithm(
            current_area_identifier
        ).do_algorithm()
        destination_area_data = get_place_full_data_algorithm_factory.create_algorithm(
            destination_identifier
        ).do_algorithm()

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

        config_loader = ConfigLoader()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            # Handle AJAX request
            action = request.form.get("submit_action")
            if action == "travel":
                TimeManager(playthrough_name).advance_time(
                    config_loader.get_time_advanced_due_to_traveling()
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
            RelevantCharactersInformationFactoryComposer(
                playthrough_name,
                "Follower",
                FollowersIdentifiersStrategy(playthrough_name),
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

        playthrough_manager = PlaythroughManager(playthrough_name)

        playthrough_manager.add_to_adventure(narrative + "\n" + outcome)

        place_manager_factory = PlaceManagerFactory(playthrough_name)

        hierarchy_manager_factory = HierarchyManagerFactory(playthrough_name)

        get_place_full_data_algorithm = GetPlaceFullDataAlgorithm(
            destination_identifier, place_manager_factory, hierarchy_manager_factory
        )

        destination_place_data = get_place_full_data_algorithm.do_algorithm()

        destination_area_name = destination_place_data["area_data"]["name"]

        # Generate voice lines in parallel using threading
        direct_voice_line_generation_algorithm_factory = (
            DirectVoiceLineGenerationAlgorithmFactory
        )

        player_character = Character(
            playthrough_name, playthrough_manager.get_player_identifier()
        )

        result_dict = {
            "narrative_voice_line_url": (
                direct_voice_line_generation_algorithm_factory.create_algorithm(
                    player_character.name,
                    product.get_narrative(),
                    player_character.voice_model,
                ).direct_voice_line_generation()
            ),
            "outcome_voice_line_url": (
                direct_voice_line_generation_algorithm_factory.create_algorithm(
                    player_character.name,
                    product.get_outcome(),
                    player_character.voice_model,
                ).direct_voice_line_generation()
            ),
        }

        narrative_voice_line_url = result_dict.get("narrative_voice_line_url")
        outcome_voice_line_url = result_dict.get("outcome_voice_line_url")

        if not isinstance(narrative_voice_line_url, Path):
            raise TypeError(
                f"Expected 'narrative_voice_line' to be a Path, but was '{type(narrative_voice_line_url)}'."
            )
        if not isinstance(outcome_voice_line_url, Path):
            raise TypeError(
                f"Expected 'outcome_voice_line_url' to be a Path, but was '{type(outcome_voice_line_url)}'."
            )

        return jsonify(
            {
                "success": True,
                "narrative": narrative,
                "outcome": outcome,
                "narrative_voice_line_url": WebService.get_file_url(
                    Path("voice_lines"), narrative_voice_line_url
                ),
                "outcome_voice_line_url": WebService.get_file_url(
                    Path("voice_lines"), outcome_voice_line_url
                ),
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

        PlaceService().visit_place(playthrough_name, destination_identifier)

        return redirect(url_for("location-hub"))
