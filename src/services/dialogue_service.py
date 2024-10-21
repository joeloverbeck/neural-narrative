from flask import session, url_for

from src.base.playthrough_manager import PlaythroughManager
from src.base.required_string import RequiredString
from src.config.config_manager import ConfigManager
from src.dialogues.commands.produce_ambient_narration_command import (
    ProduceAmbientNarrationCommand,
)
from src.dialogues.commands.setup_dialogue_command import SetupDialogueCommand
from src.dialogues.commands.store_temporary_dialogue_command import (
    StoreTemporaryDialogueCommand,
)
from src.dialogues.dialogue_manager import DialogueManager
from src.dialogues.factories.ambient_narration_provider_factory import (
    AmbientNarrationProviderFactory,
)
from src.dialogues.factories.handle_possible_existence_of_ongoing_conversation_command_factory import (
    HandlePossibleExistenceOfOngoingConversationCommandFactory,
)
from src.dialogues.factories.load_data_from_ongoing_dialogue_command_factory import (
    LoadDataFromOngoingDialogueCommandFactory,
)
from src.dialogues.factories.web_player_input_factory import WebPlayerInputFactory
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.observers.web_ambient_narration_observer import (
    WebAmbientNarrationObserver,
)
from src.dialogues.observers.web_dialogue_observer import WebDialogueObserver
from src.dialogues.participants import Participants
from src.dialogues.strategies.web_choose_participants_strategy import (
    WebChooseParticipantsStrategy,
)
from src.dialogues.strategies.web_message_data_producer_for_introduce_player_input_into_dialogue_strategy import (
    WebMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
)
from src.dialogues.strategies.web_message_data_producer_for_speech_turn_strategy import (
    WebMessageDataProducerForSpeechTurnStrategy,
)
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.place_description_manager import PlaceDescriptionManager
from src.maps.templates_repository import TemplatesRepository
from src.maps.weathers_manager import WeathersManager
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class DialogueService:
    def __init__(self):
        self._playthrough_name = session.get("playthrough_name")

        self._filesystem_manager = FilesystemManager()
        self._playthrough_manager = PlaythroughManager(self._playthrough_name)
        self._participants_instance = Participants()
        self._web_dialogue_observer = WebDialogueObserver()

    @staticmethod
    def process_ambient_message():
        # Initialize necessary objects
        messages_to_llm = MessagesToLlm()
        transcription = Transcription()
        web_ambient_narration_observer = WebAmbientNarrationObserver()

        produce_tool_response_strategy_factory = ProduceToolResponseStrategyFactory(
            OpenRouterLlmClientFactory().create_llm_client(),
            ConfigManager().get_heavy_llm(),
        )

        playthrough_name = session.get("playthrough_name")

        map_manager_factory = MapManagerFactory(RequiredString(playthrough_name))

        weathers_manager = WeathersManager(map_manager_factory)

        place_manager_factory = PlaceManagerFactory(RequiredString(playthrough_name))

        template_repository = TemplatesRepository()

        place_description_manager = PlaceDescriptionManager(
            place_manager_factory, template_repository
        )

        ambient_narration_provider_factory = AmbientNarrationProviderFactory(
            playthrough_name,
            produce_tool_response_strategy_factory,
            weathers_manager,
            place_description_manager,
        )

        dialogue_manager = DialogueManager(playthrough_name)

        participants = Participants()

        player_identifier = PlaythroughManager(playthrough_name).get_player_identifier()

        dialogue_manager.gather_participants_data(
            player_identifier, session.get("participants"), participants
        )

        load_data_from_ongoing_dialogue_command_factory = (
            LoadDataFromOngoingDialogueCommandFactory(playthrough_name, participants)
        )

        choose_participants_strategy = WebChooseParticipantsStrategy(
            session.get("participants")
        )

        handle_possible_existence_of_ongoing_conversation_command_factory = (
            HandlePossibleExistenceOfOngoingConversationCommandFactory(
                playthrough_name,
                player_identifier,
                participants,
                load_data_from_ongoing_dialogue_command_factory,
                choose_participants_strategy,
            )
        )

        store_temporary_dialogue_command = StoreTemporaryDialogueCommand(
            playthrough_name,
            participants,
            session.get("purpose", ""),
            messages_to_llm,
            transcription,
        )

        # Create and execute the command
        produce_ambient_narration_command = ProduceAmbientNarrationCommand(
            messages_to_llm,
            transcription,
            web_ambient_narration_observer,
            ambient_narration_provider_factory,
            handle_possible_existence_of_ongoing_conversation_command_factory,
            store_temporary_dialogue_command,
        )
        produce_ambient_narration_command.execute()

        # Retrieve the message from the observer
        return web_ambient_narration_observer.get_messages()[0]

    def process_user_input(self, user_input):
        # Create player input factory
        web_player_input_factory = WebPlayerInputFactory(user_input)
        player_input_product = web_player_input_factory.create_player_input()

        load_data_command_factory = LoadDataFromOngoingDialogueCommandFactory(
            self._playthrough_name, self._participants_instance
        )

        handle_possible_existence_of_ongoing_conversation_command = (
            HandlePossibleExistenceOfOngoingConversationCommandFactory(
                self._playthrough_name,
                self._playthrough_manager.get_player_identifier(),
                self._participants_instance,
                load_data_command_factory,
                WebChooseParticipantsStrategy(session.get("participants")),
            )
        )

        # Setup dialogue command
        setup_command = SetupDialogueCommand(
            self._playthrough_name,
            self._playthrough_manager.get_player_identifier(),
            self._participants_instance,
            session.get("purpose", ""),
            self._web_dialogue_observer,
            web_player_input_factory,
            handle_possible_existence_of_ongoing_conversation_command,
            WebMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy(),
            WebMessageDataProducerForSpeechTurnStrategy(
                self._playthrough_name,
                self._playthrough_manager.get_player_identifier(),
            ),
        )

        setup_command.execute()

        # Check if the input was "goodbye"
        is_goodbye = player_input_product.is_goodbye()

        # Prepare messages
        messages = self.prepare_messages()

        return messages, is_goodbye

    def prepare_messages(self):
        messages = []
        for message in self._web_dialogue_observer.get_messages():
            message["sender_photo_url"] = url_for(
                "static", filename=message["sender_photo_url"]
            )
            messages.append(message)
        return messages
