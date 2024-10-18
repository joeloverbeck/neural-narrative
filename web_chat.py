import logging.config

from flask import Flask
from flask import session, redirect, url_for, render_template, request, flash, jsonify

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
from src.actions.factories.research_resolution_factory import ResearchResolutionFactory
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.characters.participants_manager import ParticipantsManager
from src.config.config_manager import ConfigManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.views.actions_view import ActionsView
from src.views.character_generation_view import CharacterGenerationView
from src.views.character_memories_view import CharacterMemoriesView
from src.views.character_secrets_view import CharacterSecretsView
from src.views.character_voice_view import CharacterVoiceView
from src.views.characters_hub_view import CharactersHubView
from src.views.chat_view import ChatView
from src.views.connections_view import ConnectionsView
from src.views.index_view import IndexView
from src.views.location_hub_view import LocationHubView
from src.views.participants_view import ParticipantsView
from src.views.story_hub_view import StoryHubView
from src.views.travel_view import TravelView
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)

logging.config.dictConfig(FilesystemManager().get_logging_config_file())

app = Flask(__name__)

app.secret_key = b"neural-narrative"

logger = logging.getLogger(__name__)

# Register the view
app.add_url_rule("/", view_func=IndexView.as_view("index"))
app.add_url_rule("/story-hub", view_func=StoryHubView.as_view("story-hub"))
app.add_url_rule(
    "/characters-hub", view_func=CharactersHubView.as_view("characters-hub")
)
app.add_url_rule("/location-hub", view_func=LocationHubView.as_view("location-hub"))
app.add_url_rule("/travel", view_func=TravelView.as_view("travel"))
app.add_url_rule("/participants", view_func=ParticipantsView.as_view("participants"))
app.add_url_rule("/chat", view_func=ChatView.as_view("chat"))
app.add_url_rule(
    "/character-generation",
    view_func=CharacterGenerationView.as_view("character-generation"),
)
app.add_url_rule(
    "/character-memories",
    view_func=CharacterMemoriesView.as_view("character-memories"),
    methods=["GET", "POST"],
)
app.add_url_rule(
    "/character-voice", view_func=CharacterVoiceView.as_view("character-voice")
)
app.add_url_rule(
    "/character-secrets", view_func=CharacterSecretsView.as_view("character-secrets")
)
app.add_url_rule("/actions", view_func=ActionsView.as_view("actions"))
app.add_url_rule("/connections", view_func=ConnectionsView.as_view("connections"))


@app.route("/research", methods=["GET", "POST"])
def research():
    if request.method == "GET":
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        map_manager = MapManager(playthrough_name)
        current_place = map_manager.get_current_place_template()

        return render_template(
            "action.html",
            action_name="Research",
            action_icon="fa-book",
            current_place=current_place,
            action_endpoint="research",
        )
    else:
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(success=False, error="Playthrough not found."), 400
            else:
                return redirect(url_for("index"))

        form_type = request.form.get("form_type")

        if form_type == "resolve_action":
            # Handle research resolution
            research_goal = request.form.get("action_goal")
            if not research_goal:
                logger.info("Considered there was no research goal.")
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return (
                        jsonify(success=False, error="Please enter a research goal."),
                        400,
                    )
                else:
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

            players_and_followers_information_factory = (
                PlayerAndFollowersInformationFactory(party_data_for_prompt_factory)
            )

            places_descriptions_factory = PlacesDescriptionsFactory(
                place_descriptions_for_prompt_factory
            )

            research_resolution_factory = ResearchResolutionFactory(
                playthrough_name,
                research_goal,
                produce_tool_response_strategy_factory,
                places_descriptions_factory,
                players_and_followers_information_factory,
            )

            store_character_memory_command_factory = StoreCharacterMemoryCommandFactory(
                playthrough_name,
            )

            # Initialize Participants
            participants = ParticipantsManager(
                playthrough_name
            ).initialize_participants()

            store_action_resolution_algorithm = StoreActionResolutionAlgorithm(
                playthrough_name, participants, store_character_memory_command_factory
            )

            produce_voice_lines_for_action_resolution_algorithm = (
                ProduceVoiceLinesForActionResolutionAlgorithm(
                    DirectVoiceLineGenerationAlgorithmFactory()
                )
            )

            research_resolution_algorithm = ProduceActionResolutionAlgorithm(
                playthrough_name,
                research_resolution_factory,
                store_action_resolution_algorithm,
                produce_voice_lines_for_action_resolution_algorithm,
            )

            try:
                result = research_resolution_algorithm.do_algorithm()
            except ValueError as e:
                logger.error("Unexpected error: %s", e)
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(success=False, error=str(e)), 400
                else:
                    flash(str(e), "error")
                    return redirect(url_for("research"))

            # Get current place
            map_manager = MapManager(playthrough_name)
            current_place = map_manager.get_current_place_template()

            # Collect characters for modification
            player = Character(
                playthrough_name,
                PlaythroughManager(playthrough_name).get_player_identifier(),
            )

            characters_manager = CharactersManager(playthrough_name)

            character_list = [player] + characters_manager.get_followers()

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                # Return JSON response
                response_data = {
                    "success": True,
                    "message": "Research resolved successfully.",
                    "action_name": "Research",
                    "result": {
                        "narrative": result.get_narrative(),
                        "outcome": result.get_outcome(),
                        "narrative_voice_line_url": result.get_narrative_voice_line_url(),
                        "outcome_voice_line_url": result.get_outcome_voice_line_url(),
                    },
                    "current_place": current_place,
                    "characters": [
                        {
                            "identifier": char.identifier,
                            "name": char.name,
                            "description": char.description,
                            "equipment": char.equipment,
                            "health": char.health,
                        }
                        for char in character_list
                    ],
                    "form_action": url_for("research"),
                }
                return jsonify(response_data), 200
            else:
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
                follower.identifier for follower in characters_manager.get_followers()
            ]

            for identifier in character_ids:
                # Retrieve data from form
                description = request.form.get(f"description_{identifier}")
                equipment = request.form.get(f"equipment_{identifier}")
                health = request.form.get(f"health_{identifier}")

                # Load current character data
                character = Character(playthrough_name, identifier)

                # Update character data
                character.update_data({"description": description})
                character.update_data({"equipment": equipment})
                character.update_data({"health": health})

                # Save changes
                character.save()

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return (
                    jsonify(
                        success=True, message="Character changes saved successfully."
                    ),
                    200,
                )
            else:
                flash("Character changes saved successfully.", "success")
                return redirect(url_for("research"))

        else:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(success=False, error="Unknown action."), 400
            else:
                flash("Unknown action.", "error")
                return redirect(url_for("research"))


@app.route("/investigate", methods=["GET", "POST"])
def investigate():
    if request.method == "GET":
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        map_manager = MapManager(playthrough_name)
        current_place = map_manager.get_current_place_template()

        return render_template(
            "action.html",
            action_name="Investigate",
            action_icon="fa-search",
            current_place=current_place,
            action_endpoint="investigate",
        )
    else:
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(success=False, error="Playthrough not found."), 400
            else:
                return redirect(url_for("index"))

        form_type = request.form.get("form_type")

        if form_type == "resolve_action":
            # Handle investigate resolution
            investigation_goal = request.form.get("action_goal")
            if not investigation_goal:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return (
                        jsonify(
                            success=False, error="Please enter an investigation goal."
                        ),
                        400,
                    )
                else:
                    flash("Please enter an investigation goal.", "error")
                    return redirect(url_for("investigation"))

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

            players_and_followers_information_factory = (
                PlayerAndFollowersInformationFactory(party_data_for_prompt_factory)
            )

            places_descriptions_factory = PlacesDescriptionsFactory(
                place_descriptions_for_prompt_factory
            )

            investigate_resolution_factory = InvestigateResolutionFactory(
                playthrough_name,
                investigation_goal,
                produce_tool_response_strategy_factory,
                places_descriptions_factory,
                players_and_followers_information_factory,
            )

            store_character_memory_command_factory = StoreCharacterMemoryCommandFactory(
                playthrough_name,
            )

            # Initialize Participants
            participants = ParticipantsManager(
                playthrough_name
            ).initialize_participants()

            store_action_resolution_algorithm = StoreActionResolutionAlgorithm(
                playthrough_name, participants, store_character_memory_command_factory
            )

            produce_voice_lines_for_action_resolution_algorithm = (
                ProduceVoiceLinesForActionResolutionAlgorithm(
                    DirectVoiceLineGenerationAlgorithmFactory()
                )
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
                logger.error("Unexpected error: %s", e)
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(success=False, error=str(e)), 400
                else:
                    flash(str(e), "error")
                    return redirect(url_for("investigate"))

            # Get current place
            map_manager = MapManager(playthrough_name)
            current_place = map_manager.get_current_place_template()

            # Collect characters for modification
            player = Character(
                playthrough_name,
                PlaythroughManager(playthrough_name).get_player_identifier(),
            )

            characters_manager = CharactersManager(playthrough_name)

            character_list = [player] + characters_manager.get_followers()

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                # Return JSON response
                response_data = {
                    "success": True,
                    "message": "Investigate resolved successfully.",
                    "action_name": "Investigate",
                    "result": {
                        "narrative": result.get_narrative(),
                        "outcome": result.get_outcome(),
                        "narrative_voice_line_url": result.get_narrative_voice_line_url(),
                        "outcome_voice_line_url": result.get_outcome_voice_line_url(),
                    },
                    "current_place": current_place,
                    "characters": [
                        {
                            "identifier": char.identifier,
                            "name": char.name,
                            "description": char.description,
                            "equipment": char.equipment,
                            "health": char.health,
                        }
                        for char in character_list
                    ],
                    "form_action": url_for("investigate"),
                }
                return jsonify(response_data), 200
            else:
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
                follower.identifier for follower in characters_manager.get_followers()
            ]

            for identifier in character_ids:
                # Retrieve data from form
                description = request.form.get(f"description_{identifier}")
                equipment = request.form.get(f"equipment_{identifier}")
                health = request.form.get(f"health_{identifier}")

                # Load current character data
                character = Character(playthrough_name, identifier)

                # Update character data
                character.update_data({"description": description})
                character.update_data({"equipment": equipment})
                character.update_data({"health": health})

                # Save changes
                character.save()

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return (
                    jsonify(
                        success=True, message="Character changes saved successfully."
                    ),
                    200,
                )
            else:
                flash("Character changes saved successfully.", "success")
                return redirect(url_for("research"))

        else:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(success=False, error="Unknown action."), 400
            else:
                flash("Unknown action.", "error")
                return redirect(url_for("investigate"))


if __name__ == "__main__":
    app.run(debug=True)
