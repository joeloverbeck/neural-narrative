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
from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.concepts.algorithms.generate_antagonists_algorithm import (
    GenerateAntagonistsAlgorithm,
)
from src.concepts.algorithms.generate_artifacts_algorithm import (
    GenerateArtifactsAlgorithm,
)
from src.concepts.algorithms.generate_dilemmas_algorithm import (
    GenerateDilemmasAlgorithm,
)
from src.concepts.algorithms.generate_goals_algorithm import GenerateGoalsAlgorithm
from src.concepts.algorithms.generate_lore_and_legends_algorithm import (
    GenerateLoreAndLegendsAlgorithm,
)
from src.concepts.algorithms.generate_mysteries_algorithm import (
    GenerateMysteriesAlgorithm,
)
from src.concepts.algorithms.generate_plot_blueprints_algorithm import (
    GeneratePlotBlueprintsAlgorithm,
)
from src.concepts.algorithms.generate_plot_twists_algorithm import (
    GeneratePlotTwistsAlgorithm,
)
from src.concepts.algorithms.generate_scenarios_algorithm import (
    GenerateScenariosAlgorithm,
)
from src.concepts.algorithms.get_concepts_prompt_data_algorithm import (
    GetConceptsPromptDataAlgorithm,
)
from src.concepts.enums import ConceptType
from src.concepts.factories.antagonists_factory import AntagonistsFactory
from src.concepts.factories.artifacts_factory import ArtifactsFactory
from src.concepts.factories.dilemmas_factory import (
    DilemmasFactory,
)
from src.concepts.factories.goals_factory import GoalsFactory
from src.concepts.factories.lore_and_legends_factory import LoreAndLegendsFactory
from src.concepts.factories.mysteries_factory import MysteriesFactory
from src.concepts.factories.plot_blueprints_factory import PlotBlueprintsFactory
from src.concepts.factories.plot_twists_factory import PlotTwistsFactory
from src.concepts.factories.scenarios_factory import (
    ScenariosFactory,
)
from src.concepts.repositories.facts_repository import FactsRepository
from src.filesystem.file_operations import (
    create_directories,
    create_empty_json_file_if_not_exists,
    read_json_file,
    write_json_file,
)
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

        # Ensure that the concepts.json file exists.
        concepts_file_path = path_manager.get_concepts_file_path(playthrough_name_obj)

        create_empty_json_file_if_not_exists(concepts_file_path)

        data = read_json_file(concepts_file_path)

        data["facts"] = FactsRepository(playthrough_name).load_facts_file()

        return render_template("story-hub.html", **data)

    @staticmethod
    def post():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        action = request.form.get("submit_action")
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

            format_known_facts_algorithm = FormatKnownFactsAlgorithm(playthrough_name)

            get_concepts_prompt_data_algorithm = GetConceptsPromptDataAlgorithm(
                playthrough_name,
                format_known_facts_algorithm,
                places_descriptions_provider,
                player_and_followers_information_factory,
            )

            generate_action_mapping = {
                ConceptType.PLOT_BLUEPRINTS.value: {
                    "factory_class": PlotBlueprintsFactory,
                    "algorithm_class": GeneratePlotBlueprintsAlgorithm,
                    "response_key": ConceptType.PLOT_BLUEPRINTS.value,
                    "factory_args": [
                        get_concepts_prompt_data_algorithm,
                        produce_tool_response_strategy_factory,
                    ],
                },
                ConceptType.SCENARIOS.value: {
                    "factory_class": ScenariosFactory,
                    "algorithm_class": GenerateScenariosAlgorithm,
                    "response_key": ConceptType.SCENARIOS.value,
                    "factory_args": [
                        get_concepts_prompt_data_algorithm,
                        produce_tool_response_strategy_factory,
                    ],
                },
                ConceptType.DILEMMAS.value: {
                    "factory_class": DilemmasFactory,
                    "algorithm_class": GenerateDilemmasAlgorithm,
                    "response_key": ConceptType.DILEMMAS.value,
                    "factory_args": [
                        get_concepts_prompt_data_algorithm,
                        produce_tool_response_strategy_factory,
                    ],
                },
                ConceptType.GOALS.value: {
                    "factory_class": GoalsFactory,
                    "algorithm_class": GenerateGoalsAlgorithm,
                    "response_key": ConceptType.GOALS.value,
                    "factory_args": [
                        get_concepts_prompt_data_algorithm,
                        produce_tool_response_strategy_factory,
                    ],
                },
                ConceptType.PLOT_TWISTS.value: {
                    "factory_class": PlotTwistsFactory,
                    "algorithm_class": GeneratePlotTwistsAlgorithm,
                    "response_key": ConceptType.PLOT_TWISTS.value,
                    "factory_args": [
                        get_concepts_prompt_data_algorithm,
                        produce_tool_response_strategy_factory,
                    ],
                },
                ConceptType.ANTAGONISTS.value: {
                    "factory_class": AntagonistsFactory,
                    "algorithm_class": GenerateAntagonistsAlgorithm,
                    "response_key": ConceptType.ANTAGONISTS.value,
                    "factory_args": [
                        get_concepts_prompt_data_algorithm,
                        produce_tool_response_strategy_factory,
                    ],
                },
                ConceptType.LORE_AND_LEGENDS.value: {
                    "factory_class": LoreAndLegendsFactory,
                    "algorithm_class": GenerateLoreAndLegendsAlgorithm,
                    "response_key": ConceptType.LORE_AND_LEGENDS.value,
                    "factory_args": [
                        get_concepts_prompt_data_algorithm,
                        produce_tool_response_strategy_factory,
                    ],
                },
                ConceptType.ARTIFACTS.value: {
                    "factory_class": ArtifactsFactory,
                    "algorithm_class": GenerateArtifactsAlgorithm,
                    "response_key": ConceptType.ARTIFACTS.value,
                    "factory_args": [
                        get_concepts_prompt_data_algorithm,
                        produce_tool_response_strategy_factory,
                    ],
                },
                ConceptType.MYSTERIES.value: {
                    "factory_class": MysteriesFactory,
                    "algorithm_class": GenerateMysteriesAlgorithm,
                    "response_key": ConceptType.MYSTERIES.value,
                    "factory_args": [
                        get_concepts_prompt_data_algorithm,
                        produce_tool_response_strategy_factory,
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

            concepts_file_path = path_manager.get_concepts_file_path(
                playthrough_name_obj
            )

            concepts_file = read_json_file(concepts_file_path)

            key_correlation = {
                "scenario": ConceptType.SCENARIOS.value,
                "plot_twist": ConceptType.PLOT_TWISTS.value,
                "plot_blueprint": ConceptType.PLOT_BLUEPRINTS.value,
                "dilemma": ConceptType.DILEMMAS.value,
                "goal": ConceptType.GOALS.value,
                "lore_or_legend": ConceptType.LORE_AND_LEGENDS.value,
                "artifact": ConceptType.ARTIFACTS.value,
                "mystery": ConceptType.MYSTERIES.value,
            }

            key = key_correlation[action_name.lower()]

            if key in concepts_file:
                concepts_file[key].pop(index)

                # Save the file.
                write_json_file(concepts_file_path, concepts_file)
            else:
                logger.warning("'%s' wasn't in the concepts file!", action_name.lower())

            return redirect(url_for("story-hub"))
        elif action == "save_facts":
            facts = request.form.get("facts", "")
            facts = WebInterfaceManager.remove_excessive_newline_characters(facts)

            FactsRepository(playthrough_name_obj).save_facts(facts)

            flash("Facts saved.", "success")
            return redirect(url_for("story-hub"))
        else:
            return redirect(url_for("story-hub"))
