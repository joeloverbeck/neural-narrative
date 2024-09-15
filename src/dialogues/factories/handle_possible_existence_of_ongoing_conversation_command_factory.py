from src.dialogues.abstracts.strategies import ChooseParticipantsStrategy
from src.dialogues.commands.handle_possible_existence_of_ongoing_conversation_command import \
    HandlePossibleExistenceOfOngoingConversationCommand
from src.dialogues.factories.load_data_from_ongoing_dialogue_command_factory import \
    LoadDataFromOngoingDialogueCommandFactory
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription


class HandlePossibleExistenceOfOngoingConversationCommandFactory:
    def __init__(self, playthrough_name: str, player_identifier: str, participants: Participants,
                 load_data_from_ongoing_dialogue_command_factory: LoadDataFromOngoingDialogueCommandFactory,
                 choose_participants_strategy: ChooseParticipantsStrategy, ):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._load_data_from_ongoing_dialogue_command_factory = load_data_from_ongoing_dialogue_command_factory
        self._choose_participants_strategy = choose_participants_strategy

    def create_handle_possible_existence_of_ongoing_conversation_command(self, messages_to_llm: MessagesToLlm,
                                                                         transcription: Transcription) -> HandlePossibleExistenceOfOngoingConversationCommand:
        return HandlePossibleExistenceOfOngoingConversationCommand(self._playthrough_name, self._player_identifier,
                                                                   self._participants, messages_to_llm, transcription,
                                                                   self._load_data_from_ongoing_dialogue_command_factory,
                                                                   self._choose_participants_strategy)
