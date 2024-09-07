# Function definitions go here (assuming already imported or defined)
from typing import List, Any

from src.dialogues.factories.character_choice_dialogue_system_content_for_prompt_factory import \
    CharacterChoiceDialogueSystemContentForPromptFactory


def test_create_system_content_for_character_choice_dialogue_prompt():
    # Arrange
    participants = [{"name": "Jon", "identifier": "1"}, {"name": "Rusty Macy", "identifier": "2"}]
    player_identifier = 1
    dialogue: List[dict[Any, str]] = [{"Jon": "Hello!"}, {"Rusty Macy": "Hello back to you."}]
    prompt_template = """A conversation is ongoing, that features the following active participants:
{all_participants}

Here's the dialogue so far:
{dialogue}

You are tasked with determining, according to the natural flow of dialogue, who will say the next line of dialogue, among the following participants:
{participants_without_player}"""

    tool_data = {
        "type": "function",
        "function": {
            "name": "choose_speech_turn",
            "description": "chooses who among the possible participants will speak the next line of dialogue in the ongoing conversation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "identifier": {
                        "type": "integer",
                        "description": "The numeric identifier of the participant who will speak the next line of dialogue."
                    },
                    "name": {
                        "type": "string",
                        "description": "The name of the participant who will speak the next line of dialogue."
                    }
                },
                "required": [
                    "identifier",
                    "name"
                ]
            }
        }
    }

    tool_instructions_template = "{tool_name} ({tool_description})\n{tool}"

    # Expected output
    expected_output = """A conversation is ongoing, that features the following active participants:
Identifier: 1 / Name: Jon
Identifier: 2 / Name: Rusty Macy

Here's the dialogue so far:
[{'Jon': 'Hello!'}, {'Rusty Macy': 'Hello back to you.'}]

You are tasked with determining, according to the natural flow of dialogue, who will say the next line of dialogue, among the following participants:
Identifier: 2 / Name: Rusty Macy

choose_speech_turn (chooses who among the possible participants will speak the next line of dialogue in the ongoing conversation.)
{"name": "choose_speech_turn", "description": "chooses who among the possible participants will speak the next line of dialogue in the ongoing conversation.", "parameters": {"type": "object", "properties": {"identifier": {"type": "integer", "description": "The numeric identifier of the participant who will speak the next line of dialogue."}, "name": {"type": "string", "description": "The name of the participant who will speak the next line of dialogue."}}, "required": ["identifier", "name"]}}"""

    # Act
    result = CharacterChoiceDialogueSystemContentForPromptFactory(participants, player_identifier, dialogue,
                                                                  prompt_template, tool_data,
                                                                  tool_instructions_template).create_system_content_for_prompt().get()

    # Assert
    assert result == expected_output
