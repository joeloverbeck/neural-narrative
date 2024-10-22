from typing import cast
from src.base.abstracts.command import Command
from src.dialogues.commands.store_temporary_dialogue_command import StoreTemporaryDialogueCommand
from src.dialogues.factories.ambient_narration_provider_factory import AmbientNarrationProviderFactory
from src.dialogues.factories.handle_possible_existence_of_ongoing_conversation_command_factory import \
    HandlePossibleExistenceOfOngoingConversationCommandFactory
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.observers.web_ambient_narration_observer import WebAmbientNarrationObserver
from src.dialogues.products.ambient_narration_product import AmbientNarrationProduct
from src.dialogues.transcription import Transcription


class ProduceAmbientNarrationCommand(Command):

    def __init__(self, messages_to_llm: MessagesToLlm, transcription:
    Transcription, web_ambient_narration_observer:
    WebAmbientNarrationObserver, ambient_narration_provider_factory:
    AmbientNarrationProviderFactory,
                 handle_possible_existence_of_ongoing_conversation_command_factory:
                 HandlePossibleExistenceOfOngoingConversationCommandFactory,
                 store_temporary_dialogue_command: StoreTemporaryDialogueCommand):
        self._messages_to_llm = messages_to_llm
        self._transcription = transcription
        self._web_ambient_narration_observer = web_ambient_narration_observer
        self._ambient_narration_provider_factory = (
            ambient_narration_provider_factory)
        (self.
         _handle_possible_existence_of_ongoing_conversation_command_factory
         ) = (
            handle_possible_existence_of_ongoing_conversation_command_factory)
        self._store_temporary_dialogue_command = (
            store_temporary_dialogue_command)

    def execute(self) -> None:
        self._handle_possible_existence_of_ongoing_conversation_command_factory.create_handle_possible_existence_of_ongoing_conversation_command(
            self._messages_to_llm, self._transcription).execute()
        product = cast(AmbientNarrationProduct, self.
                       _ambient_narration_provider_factory.create_provider(self.
                                                                           _transcription).generate_product())
        if not product.is_valid():
            raise ValueError(
                f'Was unable to generate ambient narration. Error: {product.get_error()}'
            )
        self._web_ambient_narration_observer.update({'alignment': 'center',
                                                     'message_text': product.get()})
        self._messages_to_llm.add_message('assistant', product.get(),
                                          is_guiding_message=False)
        self._transcription.add_line(product.get())
        self._store_temporary_dialogue_command.execute()
