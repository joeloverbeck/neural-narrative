from typing import Optional

from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.abstract_factories import SystemContentForPromptProvider
from src.prompting.abstracts.factory_products import SystemContentForPromptProduct
from src.prompting.products.concrete_system_content_for_prompt_product import ConcreteSystemContentForPromptProduct
from src.tools import generate_tool_prompt


class CharacterChoiceDialogueSystemContentForPromptProvider(SystemContentForPromptProvider):

    def __init__(self, participants: Participants, player_identifier: Optional[str], transcription: Transcription,
                 prompt_template: str, tool_data: dict, tool_instructions_template: str):
        self._participants = participants
        self._player_identifier = player_identifier
        self._transcription = transcription
        self._prompt_template = prompt_template
        self._tool_data = tool_data
        self._tool_instructions_template = tool_instructions_template

    def create_system_content_for_prompt(self) -> SystemContentForPromptProduct:

        all_participants = "\n".join(
            [f"Identifier: {identifier} / Name: {participant['name']}" for identifier, participant in
             self._participants.get().items()]
        )

        if self._player_identifier:
            participants_without_player = "\n".join(
                [
                    f"Identifier: {identifier} / Name: {participant['name']} / Personality: {participant['personality']}"
                    for identifier, participant in self._participants.get().items()
                    if identifier != self._player_identifier
                ]
            )
        else:
            participants_without_player = all_participants

        if self._player_identifier:
            assert all_participants != participants_without_player

        return ConcreteSystemContentForPromptProduct(
            self._prompt_template.format(all_participants=all_participants, dialogue=self._transcription.get(),
                                         participants_without_player=participants_without_player) + "\n\n" + generate_tool_prompt(
                self._tool_data, self._tool_instructions_template), is_valid=True)
