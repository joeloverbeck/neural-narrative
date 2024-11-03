import logging
from typing import Dict, Any

from swarm import Agent
from swarm.types import Result

from src.base.validators import validate_non_empty_string
from src.writers_room.enums import AgentType

logger = logging.getLogger(__name__)


def create_agents(playthrough_name: str) -> Dict[str, Agent]:
    validate_non_empty_string(playthrough_name, "playthrough_name")

    def speech_style() -> str:
        return "You should write in a casual style, like member of a writers' room to one of his or her colleagues during creatively intense session."

    def showrunner_instructions(context_variables: Dict[str, Any]) -> str:
        return f"Context variables:{context_variables}\nInstructions: Oversee the entire creative vision of the story, lead the writing team, coordinate overarching story arcs, manage script development, and delegate tasks to your team. If the user requests working on an aspect of the story that some other agent specializes in, transfer the call to that agent. {speech_style()}"

    def story_editor_instructions(context_variables: Dict[str, Any]) -> str:
        return f"Context variables:{context_variables}\nInstructions: Refine storylines, ensure logical progression and coherence, and polish scripts for clarity and impact. {speech_style()}"

    def character_development_instructions(context_variables: Dict[str, Any]) -> str:
        return f"Context variables:{context_variables}\nInstructions: Create and deepens characters, including their arcs and relationships with others. {speech_style()}"

    def world_building_agent_instructions(context_variables: Dict[str, Any]) -> str:
        return f"Context variables:{context_variables}\nInstructions: Develop the setting, rules, and lore of the show's universe to create an immersive environment. {speech_style()}"

    def continuity_manager_agent_instructions(context_variables: Dict[str, Any]) -> str:
        return f"Context variables:{context_variables}\nInstructions: Ensure consistency in plot points, character actions, world details, and chronological sequencing. {speech_style()}"

    def researcher_agent_instructions(context_variables: Dict[str, Any]) -> str:
        return f"Context variables:{context_variables}\nInstructions: Gather relevant information, ensure factual accuracy, and integrate technical knowledge into the script. {speech_style()}"

    def theme_agent_instructions(context_variables: Dict[str, Any]) -> str:
        return f"Context variables:{context_variables}\nInstructions: Develop and weave underlying themes, messages, symbols, and motifs throughout the narrative. {speech_style()}"

    def plot_development_agent_instructions(context_variables: Dict[str, Any]) -> str:
        return f"Context variables:{context_variables}\nInstructions: Design plot elements including twists, conflicts, mysteries, and subplots to advance the story. {speech_style()}"

    def pacing_agent_instructions(context_variables: Dict[str, Any]) -> str:
        return f"Context variables:{context_variables}\nInstructions: Manage the flow of the narrative and balance emotional beats to maintain audience engagement. {speech_style()}"

    def transfer_to_showrunner_agent(**args):
        """Transfer to the Showrunner, that oversees the entire creative vision of the story, leads the writing team, coordinates overarching story arcs, and manages script development.
        Call this function if a user is asking about a topic that is not handled by the current agent.
        """
        logger.info(f"Transferring to the %s agent.", AgentType.SHOWRUNNER.value)

        result = Result()

        result.context_variables = args
        result.agent = showrunner_agent

        return result

    def transfer_to_story_editor_agent(**args):
        """Transfer to the Story Editor, that refines storylines, ensures logical progression and coherence, and polishes scripts for clarity and impact."""
        logger.info("Transferring to the %s agent.", AgentType.STORY_EDITOR.value)

        result = Result()

        result.context_variables = args
        result.agent = story_editor_agent

        return result

    def transfer_to_character_development_agent(**args):
        """Transfer to the Character Development agent, that creates and deepens characters, including their arcs and relationships with others."""
        logger.info(
            "Transferring to the %s agent.", AgentType.CHARACTER_DEVELOPMENT.value
        )

        result = Result()

        result.context_variables = args
        result.agent = character_development_agent

        return result

    def transfer_to_world_building_agent(**args):
        """Transfer to the World-Building agent, that develops the setting, rules, and lore of the story's universe to create an immersive environment."""
        logger.info("Transferring to the %s agent.", AgentType.WORLD_BUILDING.value)

        result = Result()

        result.context_variables = args
        result.agent = world_building_agent

        return result

    def transfer_to_continuity_manager_agent(**args):
        """Transfer to the Continuity Manager, that ensures consistency in plot points, character actions, world details, and chronological sequencing."""
        logger.info("Transferring to the %s agent.", AgentType.CONTINUITY_MANAGER.value)

        result = Result()

        result.context_variables = args
        result.agent = continuity_manager_agent

        return result

    def transfer_to_researcher_agent(**args):
        """Transfer to the Researcher, that gathers relevant information, ensures factual accuracy, and integrates technical knowledge into the script."""
        logger.info("Transferring to the %s agent.", AgentType.RESEARCHER.value)

        result = Result()

        result.context_variables = args
        result.agent = researcher_agent

        return result

    def transfer_to_theme_agent(**args):
        """Transfer to the Theme agent, that develops and weaves underlying themes, messages, symbols, and motifs throughout the narrative."""
        logger.info("Transferring to the %s agent.", AgentType.THEME.value)

        result = Result()

        result.context_variables = args
        result.agent = theme_agent

        return result

    def transfer_to_plot_development_agent(**args):
        """Transfer to the Plot Development agent, that designs plot elements including twists, conflicts, mysteries, and subplots to advance the story."""
        logger.info("Transferring to the %s agent.", AgentType.PLOT_DEVELOPMENT.value)

        result = Result()

        result.context_variables = args
        result.agent = plot_development_agent

        return result

    def transfer_to_pacing_agent(**args):
        """Transfer to the Pacing agent, that manages the flow of the narrative and balances emotional beats to maintain audience engagement."""
        logger.info("Transferring to the %s agent.", AgentType.PACING.value)

        result = Result()

        result.context_variables = args
        result.agent = pacing_agent

        return result

    showrunner_agent = Agent(
        name=AgentType.SHOWRUNNER.value,
        instructions=showrunner_instructions,
        functions=[
            transfer_to_story_editor_agent,
            transfer_to_character_development_agent,
            transfer_to_world_building_agent,
            transfer_to_continuity_manager_agent,
            transfer_to_researcher_agent,
            transfer_to_theme_agent,
            transfer_to_plot_development_agent,
            transfer_to_pacing_agent,
        ],
    )

    story_editor_agent = Agent(
        name=AgentType.STORY_EDITOR.value,
        instructions=story_editor_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    character_development_agent = Agent(
        name=AgentType.CHARACTER_DEVELOPMENT.value,
        instructions=character_development_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    world_building_agent = Agent(
        name=AgentType.WORLD_BUILDING.value,
        instructions=world_building_agent_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    continuity_manager_agent = Agent(
        name=AgentType.CONTINUITY_MANAGER.value,
        instructions=continuity_manager_agent_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    researcher_agent = Agent(
        name=AgentType.RESEARCHER.value,
        instructions=researcher_agent_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    theme_agent = Agent(
        name=AgentType.THEME.value,
        instructions=theme_agent_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    plot_development_agent = Agent(
        name=AgentType.PLOT_DEVELOPMENT.value,
        instructions=plot_development_agent_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    pacing_agent = Agent(
        name=AgentType.PACING.value,
        instructions=pacing_agent_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    return {
        "showrunner": showrunner_agent,
        "story_editor": story_editor_agent,
        "character_development": character_development_agent,
        "world_building": world_building_agent,
        "continuity_manager": continuity_manager_agent,
        "researcher": researcher_agent,
        "theme": theme_agent,
        "plot_development": plot_development_agent,
        "pacing": pacing_agent,
    }
