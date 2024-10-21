from src.base.required_string import RequiredString
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.abstracts.strategies import (
    MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
)
from src.dialogues.commands.introduce_player_input_into_dialogue_command import (
    IntroducePlayerInputIntoDialogueCommand,
)
from src.dialogues.transcription import Transcription


class IntroducePlayerInputIntoDialogueCommandFactory:
    def __init__(
            self,
            playthrough_name: RequiredString,
            player_identifier: RequiredString,
            message_data_producer_for_introduce_player_input_into_dialogue_strategy: MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
    ):
        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._message_data_producer_for_introduce_player_input_into_dialogue_strategy = (
            message_data_producer_for_introduce_player_input_into_dialogue_strategy
        )

    def create_introduce_player_input_into_dialogue_command(
            self, player_input_product: PlayerInputProduct, transcription: Transcription
    ) -> IntroducePlayerInputIntoDialogueCommand:
        return IntroducePlayerInputIntoDialogueCommand(
            self._playthrough_name,
            self._player_identifier,
            player_input_product,
            transcription,
            self._message_data_producer_for_introduce_player_input_into_dialogue_strategy,
        )
