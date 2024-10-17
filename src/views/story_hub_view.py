# src/views/story_hub_view
import logging
import os

from flask import session, redirect, url_for, render_template, request, jsonify, flash
from flask.views import MethodView

from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)
from src.concepts.algorithms.generate_goals_algorithm import GenerateGoalsAlgorithm
from src.concepts.algorithms.generate_interesting_dilemmas_algorithm import (
    GenerateInterestingDilemmasAlgorithm,
)
from src.concepts.algorithms.generate_interesting_situations_algorithm import (
    GenerateInterestingSituationsAlgorithm,
)
from src.concepts.algorithms.generate_plot_blueprints_algorithm import (
    GeneratePlotBlueprintsAlgorithm,
)
from src.concepts.algorithms.generate_plot_twists_algorithm import (
    GeneratePlotTwistsAlgorithm,
)
from src.concepts.factories.goals_factory import GoalsFactory
from src.concepts.factories.interesting_dilemmas_factory import (
    InterestingDilemmasFactory,
)
from src.concepts.factories.interesting_situations_factory import (
    InterestingSituationsFactory,
)
from src.concepts.factories.plot_blueprints_factory import PlotBlueprintsFactory
from src.concepts.factories.plot_twists_factory import PlotTwistsFactory
from src.config.config_manager import ConfigManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.interfaces.web_interface_manager import WebInterfaceManager
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.playthrough_name import PlaythroughName
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)

logger = logging.getLogger(__name__)


class StoryHubView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        filesystem_manager = FilesystemManager()

        # Load Plot Blueprints
        plot_blueprints = filesystem_manager.read_file_lines(
            filesystem_manager.get_file_path_to_plot_blueprints(
                PlaythroughName(playthrough_name)
            )
        )

        # Load Interesting Situations
        interesting_situations = filesystem_manager.read_file_lines(
            filesystem_manager.get_file_path_to_interesting_situations(
                PlaythroughName(playthrough_name)
            )
        )

        # Load Interesting Dilemmas
        interesting_dilemmas = filesystem_manager.read_file_lines(
            filesystem_manager.get_file_path_to_interesting_dilemmas(
                PlaythroughName(playthrough_name)
            )
        )

        # Load Goals
        goals = filesystem_manager.read_file_lines(
            filesystem_manager.get_file_path_to_goals(PlaythroughName(playthrough_name))
        )

        # Load Plot Twists
        plot_twists = filesystem_manager.read_file_lines(
            filesystem_manager.get_file_path_to_plot_twists(
                PlaythroughName(playthrough_name)
            )
        )

        # Could be that the facts don't exist.
        facts_file_path = filesystem_manager.get_file_path_to_facts(playthrough_name)

        if not os.path.exists(
            filesystem_manager.get_file_path_to_facts(playthrough_name)
        ):
            filesystem_manager.write_file(facts_file_path, "")

        # Load Facts
        facts = filesystem_manager.read_file(
            filesystem_manager.get_file_path_to_facts(playthrough_name)
        )

        return render_template(
            "story-hub.html",
            plot_blueprints=plot_blueprints,
            interesting_situations=interesting_situations,
            interesting_dilemmas=interesting_dilemmas,
            goals=goals,
            facts=facts,
            plot_twists=plot_twists,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        action = request.form.get("submit_action")

        filesystem_manager = FilesystemManager()

        if action == "generate_plot_blueprints":
            produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
                OpenRouterLlmClientFactory().create_llm_client(),
                ConfigManager().get_heavy_llm(),
            )

            player_data_for_prompt_factory = PlayerDataForPromptFactory(
                playthrough_name
            )

            party_data_for_prompt_factory = PartyDataForPromptFactory(
                playthrough_name, player_data_for_prompt_factory
            )

            place_descriptions_for_prompt_factory = PlaceDescriptionsForPromptFactory(
                playthrough_name
            )

            player_and_followers_information_factory = (
                PlayerAndFollowersInformationFactory(party_data_for_prompt_factory)
            )

            places_descriptions_factory = PlacesDescriptionsFactory(
                place_descriptions_for_prompt_factory
            )

            playthrough_name = PlaythroughName(playthrough_name)

            plot_blueprints_factory = PlotBlueprintsFactory(
                playthrough_name,
                produce_tool_response_strategy_factory,
                places_descriptions_factory,
                player_and_followers_information_factory,
            )

            algorithm = GeneratePlotBlueprintsAlgorithm(
                playthrough_name, plot_blueprints_factory
            )

            try:
                plot_blueprints = algorithm.do_algorithm()

                # Return the plot blueprints along with the response so that they get added
                # as items to the collapsible section of Plot Blueprints.
                response = {
                    "success": True,
                    "message": "Plot blueprints generated successfully.",
                    "plot_blueprints": plot_blueprints,
                }
            except Exception as e:
                response = {
                    "success": False,
                    "error": f"Failed to generate plot blueprints. Error: {str(e)}",
                }

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
            else:
                return redirect(url_for("story-hub"))
        elif action == "delete_plot_blueprint":
            plot_blueprint_index = int(request.form.get("item_index"))

            filesystem_manager = FilesystemManager()
            plot_blueprints_file_path = (
                filesystem_manager.get_file_path_to_plot_blueprints(
                    PlaythroughName(playthrough_name)
                )
            )

            if os.path.exists(plot_blueprints_file_path):
                plot_blueprints_content = filesystem_manager.read_file(
                    plot_blueprints_file_path
                )
                plot_blueprints = (
                    plot_blueprints_content.strip().split("\n")
                    if plot_blueprints_content
                    else []
                )

                if 0 <= plot_blueprint_index < len(plot_blueprints):
                    del plot_blueprints[plot_blueprint_index]
                    # Write back to file
                    filesystem_manager.write_file(
                        plot_blueprints_file_path, "\n".join(plot_blueprints)
                    )

            return redirect(url_for("story-hub"))
        elif action == "generate_situations":
            produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
                OpenRouterLlmClientFactory().create_llm_client(),
                ConfigManager().get_heavy_llm(),
            )

            player_data_for_prompt_factory = PlayerDataForPromptFactory(
                playthrough_name
            )

            party_data_for_prompt_factory = PartyDataForPromptFactory(
                playthrough_name, player_data_for_prompt_factory
            )

            place_descriptions_for_prompt_factory = PlaceDescriptionsForPromptFactory(
                playthrough_name
            )

            player_and_followers_information_factory = (
                PlayerAndFollowersInformationFactory(party_data_for_prompt_factory)
            )

            places_descriptions_factory = PlacesDescriptionsFactory(
                place_descriptions_for_prompt_factory
            )

            playthrough_name = PlaythroughName(playthrough_name)

            interesting_situations_factory = InterestingSituationsFactory(
                playthrough_name,
                produce_tool_response_strategy_factory,
                places_descriptions_factory,
                player_and_followers_information_factory,
            )

            try:
                interesting_situations = GenerateInterestingSituationsAlgorithm(
                    playthrough_name, interesting_situations_factory
                ).do_algorithm()

                response = {
                    "success": True,
                    "message": f"Generated interesting situations successfully.",
                    "interesting_situations": interesting_situations,
                }

            except Exception as e:
                logger.error(e)
                response = {
                    "success": False,
                    "error": f"Failed to generate interesting situations. Error: {str(e)}",
                }

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
            else:
                return redirect(url_for("story-hub"))

        elif action == "delete_situation":
            index = int(request.form.get("item_index"))
            filesystem_manager.remove_item_from_file(
                filesystem_manager.get_file_path_to_interesting_situations(
                    PlaythroughName(playthrough_name)
                ),
                index,
            )

            return redirect(url_for("story-hub"))
        elif action == "generate_dilemmas":
            produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
                OpenRouterLlmClientFactory().create_llm_client(),
                ConfigManager().get_heavy_llm(),
            )

            places_descriptions_for_prompt_factory = PlaceDescriptionsForPromptFactory(
                playthrough_name
            )

            player_data_for_prompt_factory = PlayerDataForPromptFactory(
                playthrough_name
            )

            party_data_for_prompt_factory = PartyDataForPromptFactory(
                playthrough_name, player_data_for_prompt_factory
            )

            player_and_followers_information_factory = (
                PlayerAndFollowersInformationFactory(party_data_for_prompt_factory)
            )

            places_descriptions_factory = PlacesDescriptionsFactory(
                places_descriptions_for_prompt_factory
            )

            playthrough_name = PlaythroughName(playthrough_name)

            interesting_dilemmas_factory = InterestingDilemmasFactory(
                playthrough_name,
                produce_tool_response_strategy_factory,
                places_descriptions_factory,
                player_and_followers_information_factory,
            )

            try:
                interesting_dilemmas = GenerateInterestingDilemmasAlgorithm(
                    playthrough_name, interesting_dilemmas_factory
                ).do_algorithm()

                response = {
                    "success": True,
                    "message": "Interesting dilemmas generated successfully.",
                    "interesting_dilemmas": interesting_dilemmas,
                }

            except Exception as e:
                response = {
                    "success": False,
                    "error": f"Failed to generate interesting dilemmas. Error: {str(e)}",
                }

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
            else:
                return redirect(url_for("story-hub"))
        elif action == "delete_dilemma":
            index = int(request.form.get("item_index"))
            filesystem_manager.remove_item_from_file(
                filesystem_manager.get_file_path_to_interesting_dilemmas(
                    PlaythroughName(playthrough_name)
                ),
                index,
            )

            return redirect(url_for("story-hub"))
        elif action == "delete_goal":
            index = int(request.form.get("item_index"))
            filesystem_manager.remove_item_from_file(
                filesystem_manager.get_file_path_to_goals(
                    PlaythroughName(playthrough_name)
                ),
                index,
            )

            return redirect(url_for("story-hub"))
        elif action == "generate_goals":
            produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
                OpenRouterLlmClientFactory().create_llm_client(),
                ConfigManager().get_heavy_llm(),
            )

            places_descriptions_for_prompt_factory = PlaceDescriptionsForPromptFactory(
                playthrough_name
            )

            player_data_for_prompt_factory = PlayerDataForPromptFactory(
                playthrough_name
            )

            party_data_for_prompt_factory = PartyDataForPromptFactory(
                playthrough_name, player_data_for_prompt_factory
            )

            places_descriptions_factory = PlacesDescriptionsFactory(
                places_descriptions_for_prompt_factory
            )

            player_and_followers_factory = PlayerAndFollowersInformationFactory(
                party_data_for_prompt_factory
            )

            playthrough_name = PlaythroughName(playthrough_name)

            goals_factory = GoalsFactory(
                playthrough_name,
                produce_tool_response_strategy_factory,
                places_descriptions_factory,
                player_and_followers_factory,
            )

            try:
                goals = GenerateGoalsAlgorithm(
                    playthrough_name, goals_factory
                ).do_algorithm()

                response = {
                    "success": True,
                    "message": "Generated goals successfully.",
                    "goals": goals,
                }
            except Exception as e:
                response = {
                    "success": False,
                    "error": f"Failed to generate goals. Error: {str(e)}",
                }

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
            else:
                return redirect(url_for("story-hub"))
        elif action == "delete_plot_twist":
            index = int(request.form.get("item_index"))
            filesystem_manager.remove_item_from_file(
                filesystem_manager.get_file_path_to_plot_twists(
                    PlaythroughName(playthrough_name)
                ),
                index,
            )

            return redirect(url_for("story-hub"))
        elif action == "generate_plot_twists":
            produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
                OpenRouterLlmClientFactory().create_llm_client(),
                ConfigManager().get_heavy_llm(),
            )

            places_descriptions_for_prompt_factory = PlaceDescriptionsForPromptFactory(
                playthrough_name
            )

            player_data_for_prompt_factory = PlayerDataForPromptFactory(
                playthrough_name
            )

            party_data_for_prompt_factory = PartyDataForPromptFactory(
                playthrough_name, player_data_for_prompt_factory
            )

            places_descriptions_factory = PlacesDescriptionsFactory(
                places_descriptions_for_prompt_factory
            )

            player_and_followers_factory = PlayerAndFollowersInformationFactory(
                party_data_for_prompt_factory
            )

            playthrough_name = PlaythroughName(playthrough_name)

            plot_twists_factory = PlotTwistsFactory(
                playthrough_name,
                produce_tool_response_strategy_factory,
                places_descriptions_factory,
                player_and_followers_factory,
            )

            try:
                plot_twists = GeneratePlotTwistsAlgorithm(
                    playthrough_name, plot_twists_factory
                ).do_algorithm()

                response = {
                    "success": True,
                    "message": "Generated plot twists successfully.",
                    "plot_twists": plot_twists,
                }
            except Exception as e:
                response = {
                    "success": False,
                    "error": f"Failed to generate plot twists. Error: {str(e)}",
                }

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
            else:
                return redirect(url_for("story-hub"))
        elif action == "save_facts":
            facts = request.form.get("facts", "")

            # Clean facts of excessive newline characters
            facts = WebInterfaceManager.remove_excessive_newline_characters(facts)

            filesystem_manager.write_file(
                filesystem_manager.get_file_path_to_facts(playthrough_name),
                facts,
            )

            flash("Facts saved.", "success")
            return redirect(url_for("story-hub"))
        else:
            return redirect(url_for("story-hub"))
