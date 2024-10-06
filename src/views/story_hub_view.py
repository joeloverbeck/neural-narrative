import os

from flask import session, redirect, url_for, render_template, request
from flask.views import MethodView

from src.config.config_manager import ConfigManager
from src.events.commands.generate_concepts_command import GenerateConceptsCommand
from src.events.factories.concepts_factory import ConceptsFactory
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
        concepts_file_path = filesystem_manager.get_file_path_to_concepts(
            playthrough_name
        )

        # Read existing concepts
        if os.path.exists(concepts_file_path):
            concepts_content = filesystem_manager.read_file(concepts_file_path)
            concepts = concepts_content.strip().split("\n") if concepts_content else []
        else:
            concepts = []

        return render_template("story-hub.html", concepts=concepts)

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        action = request.form.get("action")
        if action == "generate_concepts":
            produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
                OpenRouterLlmClientFactory().create_llm_client(),
                ConfigManager().get_heavy_llm(),
            )

            concepts_factory = ConceptsFactory(
                playthrough_name, produce_tool_response_strategy_factory
            )

            command = GenerateConceptsCommand(playthrough_name, concepts_factory)

            command.execute()

            return redirect(url_for("story-hub"))
        elif action == "delete_concept":
            concept_index = int(request.form.get("concept_index"))

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
        else:
            return redirect(url_for("story-hub"))
