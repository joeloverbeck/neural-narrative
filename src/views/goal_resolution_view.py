# views/goal_resolution_view.py

from flask import session, redirect, url_for, render_template, request, flash
from flask.views import MethodView

from src.actions.algorithms.produce_goal_resolution_algorithm import (
    ProduceGoalResolutionAlgorithm,
)
from src.actions.factories.goal_resolution_factory import GoalResolutionFactory
from src.characters.characters_manager import CharactersManager
from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.config.config_manager import ConfigManager
from src.dialogues.participants import Participants
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class GoalResolutionView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        # Get current place description
        map_manager = MapManager(playthrough_name)
        current_place = map_manager.get_current_place_template()

        return render_template("goal-resolution.html", current_place=current_place)

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        # Get the goal from the form
        goal = request.form.get("goal")
        if not goal:
            flash("Please enter a goal to resolve.", "error")
            return redirect(url_for("goal-resolution"))

        # Initialize necessary components
        produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
            OpenRouterLlmClientFactory().create_llm_client(),
            ConfigManager().get_heavy_llm(),
        )

        party_data_for_prompt_factory = PartyDataForPromptFactory(playthrough_name)
        goal_resolution_factory = GoalResolutionFactory(
            playthrough_name,
            goal,
            produce_tool_response_strategy_factory,
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
        )

        # Now do the same for the followers.
        for follower in characters_manager.get_followers():
            participants.add_participant(
                follower["identifier"],
                follower["name"],
                follower["description"],
                follower["personality"],
                follower["equipment"],
            )

        goal_resolution_algorithm = ProduceGoalResolutionAlgorithm(
            playthrough_name,
            participants,
            goal_resolution_factory,
            store_character_memory_command_factory,
        )

        try:
            result = goal_resolution_algorithm.produce_goal_resolution()
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("goal-resolution"))

        # Render the template with the result
        map_manager = MapManager(playthrough_name)
        current_place = map_manager.get_current_place_template()

        if not current_place:
            raise ValueError("The current place shouldn't be empty.")

        return render_template(
            "goal-resolution.html",
            current_place=current_place,
            result=result,
        )
