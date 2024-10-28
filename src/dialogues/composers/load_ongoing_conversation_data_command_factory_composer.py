from typing import Optional, List

from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.dialogues.factories.load_data_from_ongoing_dialogue_command_factory import (
    LoadDataFromOngoingDialogueCommandFactory,
)
from src.dialogues.factories.load_ongoing_conversation_data_command_factory import (
    LoadOngoingConversationDataCommandFactory,
)
from src.dialogues.participants import Participants
from src.dialogues.strategies.web_choose_participants_strategy import (
    WebChooseParticipantsStrategy,
)


class LoadOngoingConversationDataCommandFactoryComposer:
    def __init__(
        self,
        playthrough_name: str,
        other_characters_identifiers: List[str],
        participants: Participants,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        # Do not check if there are enough participants here! This command is going to load the data.

        self._playthrough_name = playthrough_name
        self._other_characters_identifiers = other_characters_identifiers
        self._participants = participants

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def composer_factory(
        self,
    ) -> LoadOngoingConversationDataCommandFactory:
        load_data_from_ongoing_dialogue_command_factory = (
            LoadDataFromOngoingDialogueCommandFactory(
                self._playthrough_name, self._participants
            )
        )

        choose_participants_strategy = WebChooseParticipantsStrategy(
            self._other_characters_identifiers
        )

        return LoadOngoingConversationDataCommandFactory(
            self._playthrough_name,
            self._playthrough_manager.get_player_identifier(),
            self._participants,
            load_data_from_ongoing_dialogue_command_factory,
            choose_participants_strategy,
        )
