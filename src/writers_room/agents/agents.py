from typing import Dict

from swarm import Agent

from src.base.validators import validate_non_empty_string
from src.concepts.enums import ConceptType


def create_agents(playthrough_name: str) -> Dict[str, Agent]:
    validate_non_empty_string(playthrough_name, "playthrough_name")

    def speech_style() -> str:
        return "You should write in a casual style, like member of a writers' room to one of his or her colleagues during creatively intense session."

    def showrunner_instructions(context_variables: dict) -> str:
        return f"Context:\n{context_variables.get("context")}\nPlot Blueprints Inspiration:\n{context_variables.get(ConceptType.PLOT_BLUEPRINTS.value)}\nInstructions: Oversee the entire creative vision of the story, lead the writing team, coordinate overarching story arcs, manage script development, and delegate tasks to your team. If the user requests working on an aspect of the story that some other agent specializes in, transfer the call to that agent. {speech_style()}"

    def story_editor_instructions(context_variables: dict) -> str:
        return f"Facts:\n{context_variables.get("facts")}\nInstructions: Refine storylines, ensure logical progression and coherence, and polish scripts for clarity and impact. {speech_style()}"

    def character_development_instructions(context_variables: dict) -> str:
        return f"Characters:\n{context_variables.get("characters")}\nInstructions: Create and deepens characters, including their arcs and relationships with others. {speech_style()}"

    def world_building_agent_instructions(context_variables: dict) -> str:
        return f"Places Descriptions:\n{context_variables.get("places_descriptions")}\nInstructions: Develop the setting, rules, and lore of the show's universe to create an immersive environment. {speech_style()}"

    def continuity_manager_agent_instructions(context_variables: dict) -> str:
        return f"Facts:\n{context_variables.get("facts")}\nCharacters:\n{context_variables.get("characters")}\nPlaces Descriptions:\n{context_variables.get("places_descriptions")}\nInstructions: Ensure consistency in plot points, character actions, world details, and chronological sequencing. {speech_style()}"

    def researcher_agent_instructions(context_variables: dict) -> str:
        return f"Facts:\n{context_variables.get("facts")}\nInstructions: Gather relevant information, ensure factual accuracy, and integrate technical knowledge into the script. {speech_style()}"

    def theme_agent_instructions(context_variables: dict) -> str:
        return f"Context:\n{context_variables.get("context")}\nInstructions: Develop and weave underlying themes, messages, symbols, and motifs throughout the narrative. {speech_style()}"

    def plot_development_agent_instructions(context_variables: dict) -> str:
        return f"Goals Inspiration:\n{context_variables.get(ConceptType.GOALS.value)}\nPlot Twists Inspiration:\n{context_variables.get(ConceptType.PLOT_TWISTS.value)}\nScenarios Inspiration:\n{context_variables.get(ConceptType.SCENARIOS.value)}\nInstructions: Design plot elements including twists, conflicts, mysteries, and subplots to advance the story. {speech_style()}"

    def pacing_agent_instructions(context_variables: dict) -> str:
        return f"Dilemmas Inspiration:\n{context_variables.get(ConceptType.DILEMMAS.value)}\nInstructions: Manage the flow of the narrative and balance emotional beats to maintain audience engagement. {speech_style()}"

    def transfer_to_showrunner_agent(_context_variables: dict):
        """Transfer to the Showrunner, that oversees the entire creative vision of the story, leads the writing team, coordinates overarching story arcs, and manages script development."""
        return showrunner_agent

    def transfer_to_story_editor_agent(_context_variables: dict):
        """Transfer to the Story Editor, that refines storylines, ensures logical progression and coherence, and polishes scripts for clarity and impact."""
        return story_editor_agent

    def transfer_to_character_development_agent(_context_variables: dict):
        """Transfer to the Character Development agent, that creates and deepens characters, including their arcs and relationships with others."""
        return character_development_agent

    def transfer_to_world_building_agent(_context_variables: dict):
        """Transfer to the World-Building agent, that develops the setting, rules, and lore of the story's universe to create an immersive environment."""
        return world_building_agent

    def transfer_to_continuity_manager_agent(_context_variables: dict):
        """Transfer to the Continuity Manager, that ensures consistency in plot points, character actions, world details, and chronological sequencing."""
        return continuity_manager_agent

    def transfer_to_researcher_agent(_context_variables: dict):
        """Transfer to the Researcher, that gathers relevant information, ensures factual accuracy, and integrates technical knowledge into the script."""
        return researcher_agent

    def transfer_to_theme_agent(_context_variables: dict):
        """Transfer to the Theme agent, that develops and weaves underlying themes, messages, symbols, and motifs throughout the narrative."""
        return theme_agent

    def transfer_to_plot_development_agent(_context_variables: dict):
        """Transfer to the Plot Development agent, that designs plot elements including twists, conflicts, mysteries, and subplots to advance the story."""
        return plot_development_agent

    def transfer_to_pacing_agent(_context_development: dict):
        """Transfer to the Pacing agent, that manages the flow of the narrative and balances emotional beats to maintain audience engagement."""
        return pacing_agent

    showrunner_agent = Agent(
        name="Showrunner",
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
        name="Story Editor",
        instructions=story_editor_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    character_development_agent = Agent(
        name="Character Development",
        instructions=character_development_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    world_building_agent = Agent(
        name="World-Building",
        instructions=world_building_agent_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    continuity_manager_agent = Agent(
        name="Continuity Manager",
        instructions=continuity_manager_agent_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    researcher_agent = Agent(
        name="Researcher",
        instructions=researcher_agent_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    theme_agent = Agent(
        name="Theme",
        instructions=theme_agent_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    plot_development_agent = Agent(
        name="Plot Development",
        instructions=plot_development_agent_instructions,
        functions=[transfer_to_showrunner_agent],
    )

    pacing_agent = Agent(
        name="Pacing",
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
