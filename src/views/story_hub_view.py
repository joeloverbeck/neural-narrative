import logging
import os
from pathlib import Path

from flask import session, redirect, url_for, render_template, request, jsonify, flash
from flask.views import MethodView

from src.base.tools import capture_traceback
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
from src.concepts.factories.dilemmas_factory import (
    DilemmasFactory,
)
from src.concepts.factories.goals_factory import GoalsFactory
from src.concepts.factories.plot_blueprints_factory import PlotBlueprintsFactory
from src.concepts.factories.plot_twists_factory import PlotTwistsFactory
from src.concepts.factories.scenarios_factory import (
    ScenariosFactory,
)
from src.filesystem.file_operations import read_file_lines, read_file
from src.filesystem.filesystem_manager import FilesystemManager
from src.interfaces.web_interface_manager import WebInterfaceManager
from src.maps.composers.places_descriptions_provider_composer import (
    PlacesDescriptionsProviderComposer,
)
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms

logger = logging.getLogger(__name__)


class StoryHubView(MethodView):

    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        filesystem_manager = FilesystemManager()
        playthrough_name_obj = playthrough_name
        items_to_load = [
            ("plot_blueprints", filesystem_manager.get_file_path_to_plot_blueprints),
            (
                "interesting_situations",
                filesystem_manager.get_file_path_to_interesting_situations,
            ),
            (
                "interesting_dilemmas",
                filesystem_manager.get_file_path_to_interesting_dilemmas,
            ),
            ("goals", filesystem_manager.get_file_path_to_goals),
            ("plot_twists", filesystem_manager.get_file_path_to_plot_twists),
        ]
        data = {}
        for var_name, file_path_method in items_to_load:
            file_path = file_path_method(playthrough_name_obj)
            data[var_name] = [line for line in read_file_lines(Path(file_path))]
        facts_file_path = filesystem_manager.get_file_path_to_facts(playthrough_name)
        if not os.path.exists(facts_file_path):
            filesystem_manager.write_file(facts_file_path, None)
        facts = read_file(Path(facts_file_path))
        data["facts"] = facts if facts else ""
        return render_template("story-hub.html", **data)

    @staticmethod
    def post():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        action = request.form.get("submit_action")
        filesystem_manager = FilesystemManager()
        playthrough_name_obj = playthrough_name

        llms = Llms()

        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                llms.for_concept_generation(),
            ).compose_factory()
        )

        player_data_for_prompt_factory = PlayerDataForPromptFactory(
            playthrough_name, CharacterFactory(playthrough_name_obj)
        )
        party_data_for_prompt_factory = PartyDataForPromptFactory(
            playthrough_name, player_data_for_prompt_factory
        )
        player_and_followers_information_factory = PlayerAndFollowersInformationFactory(
            party_data_for_prompt_factory
        )
        places_descriptions_provider = PlacesDescriptionsProviderComposer(
            playthrough_name
        ).compose_provider()
        if action.startswith("generate_"):
            action_name = action[len("generate_") :]
            generate_action_mapping = {
                "plot_blueprints": {
                    "factory_class": PlotBlueprintsFactory,
                    "algorithm_class": GeneratePlotBlueprintsAlgorithm,
                    "response_key": "plot_blueprints",
                    "factory_args": [
                        playthrough_name_obj,
                        produce_tool_response_strategy_factory,
                        places_descriptions_provider,
                        player_and_followers_information_factory,
                    ],
                },
                "situations": {
                    "factory_class": ScenariosFactory,
                    "algorithm_class": GenerateInterestingSituationsAlgorithm,
                    "response_key": "interesting_situations",
                    "factory_args": [
                        playthrough_name_obj,
                        produce_tool_response_strategy_factory,
                        places_descriptions_provider,
                        player_and_followers_information_factory,
                    ],
                },
                "dilemmas": {
                    "factory_class": DilemmasFactory,
                    "algorithm_class": GenerateInterestingDilemmasAlgorithm,
                    "response_key": "interesting_dilemmas",
                    "factory_args": [
                        playthrough_name_obj,
                        produce_tool_response_strategy_factory,
                        places_descriptions_provider,
                        player_and_followers_information_factory,
                    ],
                },
                "goals": {
                    "factory_class": GoalsFactory,
                    "algorithm_class": GenerateGoalsAlgorithm,
                    "response_key": "goals",
                    "factory_args": [
                        playthrough_name_obj,
                        produce_tool_response_strategy_factory,
                        places_descriptions_provider,
                        player_and_followers_information_factory,
                    ],
                },
                "plot_twists": {
                    "factory_class": PlotTwistsFactory,
                    "algorithm_class": GeneratePlotTwistsAlgorithm,
                    "response_key": "plot_twists",
                    "factory_args": [
                        playthrough_name_obj,
                        produce_tool_response_strategy_factory,
                        places_descriptions_provider,
                        player_and_followers_information_factory,
                    ],
                },
            }
            if action_name in generate_action_mapping:
                mapping = generate_action_mapping[action_name]
                factory_instance = mapping["factory_class"](*mapping["factory_args"])
                algorithm_instance = mapping["algorithm_class"](
                    playthrough_name_obj, action_name, factory_instance
                )
                try:
                    items = algorithm_instance.do_algorithm()
                    response = {
                        "success": True,
                        "message": f"{mapping['response_key'].replace('_', ' ').capitalize()} generated successfully.",
                        mapping["response_key"]: [item for item in items],
                    }
                except Exception as e:
                    capture_traceback()
                    logger.error(e)
                    response = {
                        "success": False,
                        "error": f"Failed to generate {mapping['response_key'].replace('_', ' ')}. Error: {str(e)}",
                    }
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(response)
                else:
                    return redirect(url_for("story-hub"))
        elif action.startswith("delete_"):
            action_name = action[len("delete_") :]
            index = int(request.form.get("item_index"))
            delete_action_mapping = {
                "plot_blueprint": filesystem_manager.get_file_path_to_plot_blueprints(
                    playthrough_name_obj
                ),
                "situation": filesystem_manager.get_file_path_to_interesting_situations(
                    playthrough_name_obj
                ),
                "dilemma": filesystem_manager.get_file_path_to_interesting_dilemmas(
                    playthrough_name_obj
                ),
                "goal": filesystem_manager.get_file_path_to_goals(playthrough_name_obj),
                "plot_twist": filesystem_manager.get_file_path_to_plot_twists(
                    playthrough_name_obj
                ),
            }
            if action_name in delete_action_mapping:
                file_path = delete_action_mapping[action_name]
                filesystem_manager.remove_item_from_file(file_path, index)
                return redirect(url_for("story-hub"))
        elif action == "save_facts":
            facts = request.form.get("facts", "")
            facts = WebInterfaceManager.remove_excessive_newline_characters(facts)
            filesystem_manager.write_file(
                filesystem_manager.get_file_path_to_facts(playthrough_name), facts
            )
            flash("Facts saved.", "success")
            return redirect(url_for("story-hub"))
        else:
            return redirect(url_for("story-hub"))
