from src.base.algorithms.produce_and_update_next_identifier_algorithm import (
    ProduceAndUpdateNextIdentifierAlgorithm,
)
from src.characters.commands.store_generated_character_command import (
    StoreGeneratedCharacterCommand,
)
from src.voices.algorithms.match_voice_data_to_voice_model_algorithm import (
    MatchVoiceDataToVoiceModelAlgorithm,
)


class StoreGeneratedCharacterCommandFactory:

    def __init__(
        self,
        playthrough_name: str,
        match_voice_data_to_voice_model_algorithm: MatchVoiceDataToVoiceModelAlgorithm,
        produce_and_update_next_identifier_algorithm: ProduceAndUpdateNextIdentifierAlgorithm,
    ):
        self._playthrough_name = playthrough_name
        self._match_voice_data_to_voice_model_algorithm = (
            match_voice_data_to_voice_model_algorithm
        )
        self._produce_and_update_next_identifier_algorithm = (
            produce_and_update_next_identifier_algorithm
        )

    def create_store_generated_character_command(
        self, character_data: dict
    ) -> StoreGeneratedCharacterCommand:
        return StoreGeneratedCharacterCommand(
            self._playthrough_name,
            character_data,
            self._match_voice_data_to_voice_model_algorithm,
            self._produce_and_update_next_identifier_algorithm,
        )
