import os

from flask import session, redirect, url_for, render_template, request
from flask.views import MethodView

from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.config.config_manager import ConfigManager
from src.events.commands.generate_concepts_command import GenerateConceptsCommand
from src.events.commands.generate_interesting_dilemmas_command import (
    GenerateInterestingDilemmasCommand,
)
from src.events.commands.generate_interesting_situations_command import (
    GenerateInterestingSituationsCommand,
)
from src.events.factories.concepts_factory import ConceptsFactory
from src.events.factories.interesting_dilemmas_factory import InterestingDilemmasFactory
from src.events.factories.interesting_situations_factory import (
    InterestingSituationsFactory,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class StoryHubView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        filesystem_manager = FilesystemManager()

        # Load Concepts
        concepts = filesystem_manager.read_file_lines(
            filesystem_manager.get_file_path_to_concepts(playthrough_name)
        )

        # Load Interesting Situations
        interesting_situations = filesystem_manager.read_file_lines(
            filesystem_manager.get_file_path_to_interesting_situations(playthrough_name)
        )

        # Load Interesting Dilemmas
        interesting_dilemmas = filesystem_manager.read_file_lines(
            filesystem_manager.get_file_path_to_interesting_dilemmas(playthrough_name)
        )

        return render_template(
            "story-hub.html",
            concepts=concepts,
            interesting_situations=interesting_situations,
            interesting_dilemmas=interesting_dilemmas,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        action = request.form.get("action")

        filesystem_manager = FilesystemManager()

        if action == "generate_concepts":
            produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
                OpenRouterLlmClientFactory().create_llm_client(),
                ConfigManager().get_heavy_llm(),
            )

            party_data_for_prompty_factory = PartyDataForPromptFactory(playthrough_name)

            concepts_factory = ConceptsFactory(
                playthrough_name,
                produce_tool_response_strategy_factory,
                party_data_for_prompty_factory,
            )

            command = GenerateConceptsCommand(playthrough_name, concepts_factory)

            command.execute()

            return redirect(url_for("story-hub"))
        elif action == "delete_concept":
            concept_index = int(request.form.get("item_index"))

            filesystem_manager = FilesystemManager()
            concepts_file_path = filesystem_manager.get_file_path_to_concepts(
                playthrough_name
            )

            if os.path.exists(concepts_file_path):
                concepts_content = filesystem_manager.read_file(concepts_file_path)
                concepts = (
                    concepts_content.strip().split("\n") if concepts_content else []
                )

                if 0 <= concept_index < len(concepts):
                    del concepts[concept_index]
                    # Write back to file
                    filesystem_manager.write_file(
                        concepts_file_path, "\n".join(concepts)
                    )

            return redirect(url_for("story-hub"))
        elif action == "generate_situations":
            produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
                OpenRouterLlmClientFactory().create_llm_client(),
                ConfigManager().get_heavy_llm(),
            )

            party_data_for_prompty_factory = PartyDataForPromptFactory(playthrough_name)

            interesting_situations_factory = InterestingSituationsFactory(
                playthrough_name,
                produce_tool_response_strategy_factory,
                party_data_for_prompty_factory,
            )

            GenerateInterestingSituationsCommand(
                playthrough_name, interesting_situations_factory
            ).execute()

            return redirect(url_for("story-hub"))

        elif action == "delete_situation":
            index = int(request.form.get("item_index"))
            filesystem_manager.remove_item_from_file(
                filesystem_manager.get_file_path_to_interesting_situations(
                    playthrough_name
                ),
                index,
            )

            return redirect(url_for("story-hub"))
        elif action == "generate_dilemmas":
            produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
                OpenRouterLlmClientFactory().create_llm_client(),
                ConfigManager().get_heavy_llm(),
            )

            party_data_for_prompt_factory = PartyDataForPromptFactory(playthrough_name)

            interesting_dilemmas_factory = InterestingDilemmasFactory(
                playthrough_name,
                produce_tool_response_strategy_factory,
                party_data_for_prompt_factory,
            )

            GenerateInterestingDilemmasCommand(
                playthrough_name, interesting_dilemmas_factory
            ).execute()

            return redirect(url_for("story-hub"))
        elif action == "delete_dilemma":
            index = int(request.form.get("item_index"))
            filesystem_manager.remove_item_from_file(
                filesystem_manager.get_file_path_to_interesting_dilemmas(
                    playthrough_name
                ),
                index,
            )

            return redirect(url_for("story-hub"))
        else:
            return redirect(url_for("story-hub"))
