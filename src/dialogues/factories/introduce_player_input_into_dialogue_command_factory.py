from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.commands.introduce_player_input_into_dialogue_command import IntroducePlayerInputIntoDialogueCommand
from src.dialogues.transcription import Transcription


class IntroducePlayerInputIntoDialogueCommandFactory:
    def __init__(self, playthrough_name: str, player_identifier: str):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier

    def create_introduce_player_input_into_dialogue_command(self,
                                                            player_input_product: PlayerInputProduct,
                                                            transcription: Transcription) -> IntroducePlayerInputIntoDialogueCommand:
        return IntroducePlayerInputIntoDialogueCommand(
            self._playthrough_name, self._player_identifier, player_input_product, transcription)