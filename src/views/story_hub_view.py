import logging

from flask import session, redirect, url_for, render_template, request, jsonify, flash
from flask.views import MethodView

from src.base.tools import capture_traceback
from src.characters.composers.relevant_characters_information_factory_composer import (
    RelevantCharactersInformationFactoryComposer,
)
from src.characters.strategies.followers_identifiers_strategy import (
    FollowersIdentifiersStrategy,
)
from src.concepts.algorithms.generate_dilemmas_algorithm import (
    GenerateDilemmasAlgorithm,
)
from src.concepts.algorithms.generate_goals_algorithm import GenerateGoalsAlgorithm
from src.concepts.algorithms.generate_plot_blueprints_algorithm import (
    GeneratePlotBlueprintsAlgorithm,
)
from src.concepts.algorithms.generate_plot_twists_algorithm import (
    GeneratePlotTwistsAlgorithm,
)
from src.concepts.algorithms.generate_scenarios_algorithm import (
    GenerateScenariosAlgorithm,
)
from src.concepts.enums import ConceptType
from src.concepts.factories.dilemmas_factory import (
    DilemmasFactory,
)
from src.concepts.factories.goals_factory import GoalsFactory
from src.concepts.factories.plot_blueprints_factory import PlotBlueprintsFactory
from src.concepts.factories.plot_twists_factory import PlotTwistsFactory
from src.concepts.factories.scenarios_factory import (
    ScenariosFactory,
)
from src.filesystem.file_operations import (
    read_file_lines,
    read_file,
    write_file,
    create_directories,
    create_empty_file_if_not_exists,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.filesystem.path_manager import PathManager
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

    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        playthrough_name_obj = playthrough_name

        path_manager = PathManager()

        concepts_path = path_manager.get_concepts_path(playthrough_name_obj)
        create_directories(concepts_path)

        plot_blueprints_path = path_manager.get_concept_file_path(
            playthrough_name_obj, ConceptType.PLOT_BLUEPRINTS
        )

        create_empty_file_if_not_exists(plot_blueprints_path)

        scenarios_path = path_manager.get_concept_file_path(
            playthrough_name_obj, ConceptType.SCENARIOS
        )

        create_empty_file_if_not_exists(scenarios_path)

        dilemmas_path = path_manager.get_concept_file_path(
            playthrough_name_obj, ConceptType.DILEMMAS
        )

        create_empty_file_if_not_exists(dilemmas_path)

        goals_path = path_manager.get_concept_file_path(
            playthrough_name_obj, ConceptType.GOALS
        )

        create_empty_file_if_not_exists(goals_path)

        plot_twists_path = path_manager.get_concept_file_path(
            playthrough_name_obj, ConceptType.PLOT_TWISTS
        )

        create_empty_file_if_not_exists(plot_twists_path)

        items_to_load = [
            ("plot_blueprints", plot_blueprints_path),
            (
                "scenarios",
                scenarios_path,
            ),
            (
                "dilemmas",
                dilemmas_path,
            ),
            ("goals", goals_path),
            ("plot_twists", plot_twists_path),
        ]
        data = {}
        for var_name, file_path in items_to_load:
            data[var_name] = [line for line in read_file_lines(file_path)]

        facts_file_path = path_manager.get_facts_path(playthrough_name_obj)

        create_empty_file_if_not_exists(facts_file_path)

        facts = read_file(facts_file_path)

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

        player_and_followers_information_factory = (
            RelevantCharactersInformationFactoryComposer(
                playthrough_name,
                "Follower",
                FollowersIdentifiersStrategy(playthrough_name),
            ).compose_factory()
        )

        places_descriptions_provider = PlacesDescriptionsProviderComposer(
            playthrough_name
        ).compose_provider()

        path_manager = PathManager()

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
                "scenarios": {
                    "factory_class": ScenariosFactory,
                    "algorithm_class": GenerateScenariosAlgorithm,
                    "response_key": "scenarios",
                    "factory_args": [
                        playthrough_name_obj,
                        produce_tool_response_strategy_factory,
                        places_descriptions_provider,
                        player_and_followers_information_factory,
                    ],
                },
                "dilemmas": {
                    "factory_class": DilemmasFactory,
                    "algorithm_class": GenerateDilemmasAlgorithm,
                    "response_key": "dilemmas",
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
                    items = algorithm_instance.direct()
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
                "plot_blueprint": path_manager.get_concept_file_path(
                    playthrough_name_obj, ConceptType.PLOT_BLUEPRINTS
                ),
                "scenario": path_manager.get_concept_file_path(
                    playthrough_name_obj, ConceptType.SCENARIOS
                ),
                "dilemma": path_manager.get_concept_file_path(
                    playthrough_name_obj, ConceptType.DILEMMAS
                ),
                "goal": path_manager.get_concept_file_path(
                    playthrough_name_obj, ConceptType.GOALS
                ),
                "plot_twist": path_manager.get_concept_file_path(
                    playthrough_name_obj, ConceptType.PLOT_TWISTS
                ),
            }
            if action_name in delete_action_mapping:
                file_path = delete_action_mapping[action_name]
                filesystem_manager.remove_item_from_file(file_path, index)
                return redirect(url_for("story-hub"))
        elif action == "save_facts":
            facts = request.form.get("facts", "")
            facts = WebInterfaceManager.remove_excessive_newline_characters(facts)
            write_file(path_manager.get_facts_path(playthrough_name_obj), facts)
            flash("Facts saved.", "success")
            return redirect(url_for("story-hub"))
        else:
            return redirect(url_for("story-hub"))
