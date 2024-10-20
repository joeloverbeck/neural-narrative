import logging

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
from src.actions.factories.action_resolution_factory import ActionResolutionFactory
from src.base.playthrough_manager import PlaythroughManager
from src.base.required_string import RequiredString
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
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
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.characters.participants_manager import ParticipantsManager
from src.config.config_manager import ConfigManager
from src.maps.composers.places_descriptions_provider_composer import (
    PlacesDescriptionsProviderComposer,
)
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)

logger = logging.getLogger(__name__)


def action_view(action_name, action_icon, action_endpoint, prompt_file, tool_file):
    if request.method == "GET":
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        current_place = (
            MapManagerFactory(RequiredString(playthrough_name))
            .create_map_manager()
            .get_current_place_template()
        )

        return render_template(
            "action.html",
            action_name=action_name,
            action_icon=action_icon,
            current_place=current_place,
            action_endpoint=action_endpoint,
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
            # Handle action resolution
            action_goal = request.form.get("action_goal")
            if not action_goal:
                logger.info(f"No {action_name.lower()} goal provided.")
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return (
                        jsonify(
                            success=False,
                            error=f"Please enter a {action_name.lower()} goal.",
                        ),
                        400,
                    )
                else:
                    flash(f"Please enter a {action_name.lower()} goal.", "error")
                    return redirect(url_for(action_endpoint))

            # Initialize necessary components
            produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
                OpenRouterLlmClientFactory().create_llm_client(),
                ConfigManager().get_heavy_llm(),
            )

            player_data_for_prompt_factory = PlayerDataForPromptFactory(
                playthrough_name, CharacterFactory(RequiredString(playthrough_name))
            )
            party_data_for_prompt_factory = PartyDataForPromptFactory(
                playthrough_name, player_data_for_prompt_factory
            )

            players_and_followers_information_factory = (
                PlayerAndFollowersInformationFactory(party_data_for_prompt_factory)
            )

            action_resolution_factory = ActionResolutionFactory(
                playthrough_name=RequiredString(playthrough_name),
                action_name=action_name,
                action_goal=action_goal,
                produce_tool_response_strategy_factory=produce_tool_response_strategy_factory,
                places_descriptions_factory=PlacesDescriptionsProviderComposer(
                    RequiredString(playthrough_name)
                ).compose_provider(),
                players_and_followers_information_factory=players_and_followers_information_factory,
                prompt_file=prompt_file,
                tool_file=tool_file,
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

            action_resolution_algorithm = ProduceActionResolutionAlgorithm(
                playthrough_name,
                action_resolution_factory,
                store_action_resolution_algorithm,
                produce_voice_lines_for_action_resolution_algorithm,
            )

            try:
                result = action_resolution_algorithm.do_algorithm()
            except ValueError as e:
                logger.error("Unexpected error: %s", e)
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(success=False, error=str(e)), 400
                else:
                    flash(str(e), "error")
                    return redirect(url_for(action_endpoint))

            # Get current place
            current_place = (
                MapManagerFactory(RequiredString(playthrough_name))
                .create_map_manager()
                .get_current_place_template()
            )

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
                    "message": f"{action_name} resolved successfully.",
                    "action_name": action_name,
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
                    "form_action": url_for(action_endpoint),
                }
                return jsonify(response_data), 200
            else:
                return render_template(
                    f"{action_endpoint}.html",  # Adjust the template name if necessary
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
                return redirect(url_for(action_endpoint))

        else:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(success=False, error="Unknown action."), 400
            else:
                flash("Unknown action.", "error")
                return redirect(url_for(action_endpoint))
