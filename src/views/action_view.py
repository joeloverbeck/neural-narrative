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
from src.actions.models.gather_supplies import GatherSupplies
from src.actions.models.investigate import Investigate
from src.actions.models.research import Research
from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.characters.composers.relevant_characters_information_factory_composer import (
    RelevantCharactersInformationFactoryComposer,
)
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.characters.participants_manager import ParticipantsManager
from src.characters.strategies.followers_identifiers_strategy import (
    FollowersIdentifiersStrategy,
)
from src.maps.composers.places_descriptions_provider_composer import (
    PlacesDescriptionsProviderComposer,
)
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)

logger = logging.getLogger(__name__)


def action_view(action_name, action_icon, action_endpoint, prompt_file):
    if request.method == "GET":
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        current_place = (
            MapManagerFactory(playthrough_name)
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

            llms = Llms()

            produce_tool_response_strategy_factory = (
                ProduceToolResponseStrategyFactoryComposer(
                    llms.for_action_resolution()
                ).compose_factory()
            )

            players_and_followers_information_factory = (
                RelevantCharactersInformationFactoryComposer(
                    playthrough_name,
                    "Follower",
                    FollowersIdentifiersStrategy(playthrough_name),
                ).compose_factory()
            )

            action_resolution_factory = ActionResolutionFactory(
                playthrough_name=playthrough_name,
                action_name=action_name,
                action_goal=action_goal,
                produce_tool_response_strategy_factory=produce_tool_response_strategy_factory,
                places_descriptions_factory=PlacesDescriptionsProviderComposer(
                    playthrough_name
                ).compose_provider(),
                players_and_followers_information_factory=players_and_followers_information_factory,
                prompt_file=prompt_file,
            )
            store_character_memory_command_factory = StoreCharacterMemoryCommandFactory(
                playthrough_name
            )
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
                if action_name.lower() == "investigate":
                    result = action_resolution_algorithm.do_algorithm(Investigate)
                elif action_name.lower() == "research":
                    result = action_resolution_algorithm.do_algorithm(Research)
                elif action_name.lower() == "gather supplies":
                    result = action_resolution_algorithm.do_algorithm(GatherSupplies)
                else:
                    raise NotImplementedError(
                        f"Action resolution algorithm not handled for action name '{action_name}'."
                    )
            except ValueError as e:
                logger.error("Unexpected error: %s", e)
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(success=False, error=str(e)), 400
                else:
                    flash(str(e), "error")
                    return redirect(url_for(action_endpoint))
            current_place = (
                MapManagerFactory(playthrough_name)
                .create_map_manager()
                .get_current_place_template()
            )
            player = Character(
                playthrough_name,
                PlaythroughManager(playthrough_name).get_player_identifier(),
            )
            characters_manager = CharactersManager(playthrough_name)
            character_list = [player] + characters_manager.get_followers()
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
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
                    f"{action_endpoint}.html",
                    current_place=current_place,
                    result=result,
                    characters=character_list,
                )
        elif form_type == "modify_characters":
            characters_manager = CharactersManager(playthrough_name)
            playthrough_manager = PlaythroughManager(playthrough_name)
            player_identifier = playthrough_manager.get_player_identifier()
            character_ids = [player_identifier] + [
                follower.identifier for follower in characters_manager.get_followers()
            ]
            for identifier in character_ids:
                description = request.form.get(f"description_{identifier}")
                equipment = request.form.get(f"equipment_{identifier}")
                health = request.form.get(f"health_{identifier}")
                character = Character(playthrough_name, identifier)
                character.update_data({"description": description})
                character.update_data({"equipment": equipment})
                character.update_data({"health": health})
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
        elif request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify(success=False, error="Unknown action."), 400
        else:
            flash("Unknown action.", "error")
            return redirect(url_for(action_endpoint))
