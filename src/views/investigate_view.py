from flask import session, redirect, url_for, render_template, request, flash
from flask.views import MethodView

from src.actions.algorithms.produce_action_resolution_algorithm import (
    ProduceActionResolutionAlgorithm,
)
from src.actions.algorithms.produce_voice_lines_for_action_resolution_algorithm import (
    ProduceVoiceLinesForActionResolutionAlgorithm,
)
from src.actions.algorithms.store_action_resolution_algorithm import (
    StoreActionResolutionAlgorithm,
)
from src.actions.factories.investigate_resolution_factory import (
    InvestigateResolutionFactory,
)
from src.characters.characters_manager import CharactersManager
from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.config.config_manager import ConfigManager
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class InvestigateView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        map_manager = MapManager(playthrough_name)
        current_place = map_manager.get_current_place_template()

        return render_template("investigate.html", current_place=current_place)

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        form_type = request.form.get("form_type")

        if form_type == "resolve_investigate":
            # Handle investigate resolution
            investigation_goal = request.form.get("investigation_goal")
            if not investigation_goal:
                flash("Please enter an investigation goal.", "error")
                return redirect(url_for("investigate"))

            # Initialize necessary components
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

            facts_already_known = request.form.get("facts_already_known")

            investigate_resolution_factory = InvestigateResolutionFactory(
                playthrough_name,
                investigation_goal,
                facts_already_known,
                produce_tool_response_strategy_factory,
                place_descriptions_for_prompt_factory,
                party_data_for_prompt_factory,
            )

            store_character_memory_command_factory = StoreCharacterMemoryCommandFactory(
                playthrough_name,
            )

            characters_manager = CharactersManager(playthrough_name)

            # Initialize Participants
            participants = (
                characters_manager.initialize_participants_for_action_resolution()
            )

            store_action_resolution_algorithm = StoreActionResolutionAlgorithm(
                playthrough_name, participants, store_character_memory_command_factory
            )

            produce_voice_lines_for_action_resolution_algorithm = (
                ProduceVoiceLinesForActionResolutionAlgorithm()
            )

            investigate_resolution_algorithm = ProduceActionResolutionAlgorithm(
                playthrough_name,
                investigate_resolution_factory,
                store_action_resolution_algorithm,
                produce_voice_lines_for_action_resolution_algorithm,
            )

            try:
                result = investigate_resolution_algorithm.do_algorithm()
            except ValueError as e:
                flash(str(e), "error")
                return redirect(url_for("investigate"))

            # Get current place
            map_manager = MapManager(playthrough_name)
            current_place = map_manager.get_current_place_template()

            # Collect characters for modification
            player_data = characters_manager.load_character_data(
                PlaythroughManager(playthrough_name).get_player_identifier()
            )

            character_list = [player_data] + characters_manager.get_followers()

            return render_template(
                "investigate.html",
                current_place=current_place,
                result=result,
                characters=character_list,
            )

        elif form_type == "modify_characters":
            # Handle character modification
            characters_manager = CharactersManager(playthrough_name)
            playthrough_manager = PlaythroughManager(playthrough_name)

            # Get character identifiers
            player_identifier = playthrough_manager.get_player_identifier()
            character_ids = [player_identifier] + [
                follower["identifier"]
                for follower in characters_manager.get_followers()
            ]

            for identifier in character_ids:
                # Retrieve data from form
                description = request.form.get(f"description_{identifier}")
                equipment = request.form.get(f"equipment_{identifier}")
                health = request.form.get(f"health_{identifier}")

                # Load current character data
                character_data = characters_manager.load_character_data(identifier)

                # Update character data
                character_data["description"] = description
                character_data["equipment"] = equipment
                character_data["health"] = health

                # Save changes
                characters_manager.save_character_data(identifier, character_data)

            flash("Character changes saved successfully.", "success")
            return redirect(url_for("investigate"))

        else:
            flash("Unknown action.", "error")
            return redirect(url_for("investigate"))