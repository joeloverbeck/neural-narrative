from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.commands.speech_turn_produce_messages_to_prompt_llm_command import \
    SpeechTurnProduceMessagesToPromptLlmCommand
from src.dialogues.factories.determine_system_message_for_speech_turn_strategy_factory import \
    DetermineSystemMessageForSpeechTurnStrategyFactory
from src.dialogues.factories.determine_user_messages_for_speech_turn_strategy_factory import \
    DetermineUserMessagesForSpeechTurnStrategyFactory
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.factory_products import LlmToolResponseProduct


class SpeechTurnProduceMessagesToPromptLlmCommandFactory:
    def __init__(self,
                 determine_system_message_for_speech_turn_strategy_factory: DetermineSystemMessageForSpeechTurnStrategyFactory,
                 determine_user_messages_for_speech_turn_strategy_factory: DetermineUserMessagesForSpeechTurnStrategyFactory):
        self._determine_system_message_for_speech_turn_strategy_factory = determine_system_message_for_speech_turn_strategy_factory
        self._determine_user_messages_for_speech_turn_strategy_factory = determine_user_messages_for_speech_turn_strategy_factory

    def create_speech_turn_produce_messages_to_prompt_llm_command(self, messages_to_llm: MessagesToLlm,
                                                                  transcription: Transcription,
                                                                  player_input_product: PlayerInputProduct,
                                                                  speech_turn_choice_tool_response_product: LlmToolResponseProduct) -> SpeechTurnProduceMessagesToPromptLlmCommand:
        return SpeechTurnProduceMessagesToPromptLlmCommand(transcription,
                                                           speech_turn_choice_tool_response_product,
                                                           self._determine_system_message_for_speech_turn_strategy_factory.create_determine_system_message_for_speech_turn_strategy(
                                                               messages_to_llm),
                                                           self._determine_user_messages_for_speech_turn_strategy_factory.create_determine_user_messages_for_speech_turn_strategy(
                                                               player_input_product, messages_to_llm))
