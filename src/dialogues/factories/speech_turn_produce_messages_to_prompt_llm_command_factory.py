from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.commands.speech_turn_produce_messages_to_prompt_llm_command import \
    SpeechTurnProduceMessagesToPromptLlmCommand
from src.dialogues.factories.determine_system_message_for_speech_turn_strategy_factory import \
    DetermineSystemMessageForSpeechTurnStrategyFactory
from src.dialogues.factories.determine_user_messages_for_speech_turn_strategy_factory import \
    DetermineUserMessagesForSpeechTurnStrategyFactory
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.transcription import Transcription
from src.prompting.factories.speech_turn_choice_tool_response_provider_factory import \
    SpeechTurnChoiceToolResponseProviderFactory


class SpeechTurnProduceMessagesToPromptLlmCommandFactory:
    def __init__(self, speech_turn_choice_tool_response_provider_factory: SpeechTurnChoiceToolResponseProviderFactory,
                 determine_system_message_for_speech_turn_strategy_factory: DetermineSystemMessageForSpeechTurnStrategyFactory,
                 determine_user_messages_for_speech_turn_strategy_factory: DetermineUserMessagesForSpeechTurnStrategyFactory):
        self._speech_turn_choice_tool_response_provider_factory = speech_turn_choice_tool_response_provider_factory
        self._determine_system_message_for_speech_turn_strategy_factory = determine_system_message_for_speech_turn_strategy_factory
        self._determine_user_messages_for_speech_turn_strategy_factory = determine_user_messages_for_speech_turn_strategy_factory

    def create_speech_turn_produce_messages_to_prompt_llm_command(self, messages_to_llm: MessagesToLlm,
                                                                  transcription: Transcription,
                                                                  player_input_product: PlayerInputProduct) -> SpeechTurnProduceMessagesToPromptLlmCommand:
        return SpeechTurnProduceMessagesToPromptLlmCommand(transcription,
                                                           self._speech_turn_choice_tool_response_provider_factory,
                                                           self._determine_system_message_for_speech_turn_strategy_factory.create_determine_system_message_for_speech_turn_strategy(
                                                               messages_to_llm),
                                                           self._determine_user_messages_for_speech_turn_strategy_factory.create_determine_user_messages_for_speech_turn_strategy(
                                                               player_input_product, messages_to_llm))
