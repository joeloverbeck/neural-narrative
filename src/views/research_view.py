from flask import session, redirect, url_for, render_template, request, flash
from flask.views import MethodView

from src.actions.algorithms.produce_research_resolution_algorithm import (
    ProduceResearchResolutionAlgorithm,
)
from src.actions.factories.research_resolution_factory import ResearchResolutionFactory
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
from src.dialogues.participants import Participants
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


class ResearchView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        map_manager = MapManager(playthrough_name)
        current_place = map_manager.get_current_place_template()

        return render_template("research.html", current_place=current_place)

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        form_type = request.form.get("form_type")

        if form_type == "resolve_research":
            # Handle research resolution
            research_goal = request.form.get("research_goal")
            if not research_goal:
                flash("Please enter a research goal.", "error")
                return redirect(url_for("research"))

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
            research_resolution_factory = ResearchResolutionFactory(
                playthrough_name,
                research_goal,
                produce_tool_response_strategy_factory,
                place_descriptions_for_prompt_factory,
                party_data_for_prompt_factory,
            )

            store_character_memory_command_factory = StoreCharacterMemoryCommandFactory(
                playthrough_name,
            )

            # Initialize Participants
            participants = Participants()
            characters_manager = CharactersManager(playthrough_name)
            playthrough_manager = PlaythroughManager(playthrough_name)

            player_data = characters_manager.load_character_data(
                playthrough_manager.get_player_identifier()
            )

            participants.add_participant(
                player_data["identifier"],
                player_data["name"],
                player_data["description"],
                player_data["personality"],
                player_data["equipment"],
                player_data.get("voice_model", ""),
            )

            for follower in characters_manager.get_followers():
                participants.add_participant(
                    follower["identifier"],
                    follower["name"],
                    follower["description"],
                    follower["personality"],
                    follower["equipment"],
                    follower.get("voice_model", ""),
                )

            research_resolution_algorithm = ProduceResearchResolutionAlgorithm(
                playthrough_name,
                participants,
                research_resolution_factory,
                store_character_memory_command_factory,
            )

            try:
                result = research_resolution_algorithm.do_algorithm()
            except ValueError as e:
                flash(str(e), "error")
                return redirect(url_for("research"))

            # Get current place
            map_manager = MapManager(playthrough_name)
            current_place = map_manager.get_current_place_template()

            # Collect characters for modification
            character_list = [player_data] + characters_manager.get_followers()

            return render_template(
                "research.html",
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
            return redirect(url_for("research"))

        else:
            flash("Unknown action.", "error")
            return redirect(url_for("research"))
