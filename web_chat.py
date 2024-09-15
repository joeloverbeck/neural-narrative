import os
from typing import List

from flask import Flask, request, redirect, url_for, render_template, session

from src.characters.characters_manager import CharactersManager
from src.constants import MAX_DIALOGUE_ENTRIES_FOR_WEB
from src.dialogues.abstracts.factory_products import PlayerInputProduct, SpeechDataProduct
from src.dialogues.abstracts.strategies import MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy, \
    MessageDataProducerForSpeechTurnStrategy
from src.dialogues.commands.setup_dialogue_command import SetupDialogueCommand
from src.dialogues.factories.web_player_input_factory import WebPlayerInputFactory
from src.dialogues.participants import Participants
from src.dialogues.strategies.web_choose_participants_strategy import WebChooseParticipantsStrategy
from src.filesystem.filesystem_manager import FilesystemManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.abstracts.factory_products import LlmToolResponseProduct

app = Flask(__name__)

app.secret_key = b'neural-narrative'

from src.abstracts.observer import Observer


class WebMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy(
    MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy):
    def produce_message_data(self, player_character_data: dict, player_input_product: PlayerInputProduct) -> dict:
        return {
            'alignment': 'right',
            'sender_name': player_character_data['name'],
            'sender_photo_url': player_character_data['image_url'],
            'message_text': player_input_product.get()
        }


class WebMessageDataProducerForSpeechTurnStrategy(MessageDataProducerForSpeechTurnStrategy):
    def __init__(self, playthrough_name: str, filesystem_manager: FilesystemManager = None):
        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def produce_message_data(self, speech_turn_choice_tool_response_product: LlmToolResponseProduct,
                             speech_data_product: SpeechDataProduct) -> dict[str, str]:
        image_url = self._filesystem_manager.get_file_path_to_character_image_for_web(self._playthrough_name,
                                                                                      speech_turn_choice_tool_response_product.get()[
                                                                                          "identifier"])

        return {
            'alignment': 'left',
            'sender_name': speech_data_product.get()['name'],
            'sender_photo_url': image_url,
            'message_text': f"*{speech_data_product.get()['narration_text']}* {speech_data_product.get()['speech']} "
        }


class WebDialogueObserver(Observer):
    def __init__(self):
        self._messages = []
        self._characters_manager = CharactersManager(session.get('playthrough_name'))

    def update(self, message: dict) -> None:
        # alignment = 'left' if sender_id != 'player' else 'right'

        self._messages.append({
            'alignment': message['alignment'],
            'sender_name': message['sender_name'],
            'sender_photo_url': message['sender_photo_url'],
            'message_text': message['message_text']
        })

    def get_messages(self) -> List[dict]:
        return self._messages


@app.route('/', methods=['GET', 'POST'])
def index():
    filesystem_manager = FilesystemManager()
    playthroughs_folder = filesystem_manager.get_file_path_to_playthroughs_folder()

    # Retrieve the list of existing playthrough folders
    if os.path.exists(playthroughs_folder):
        playthrough_names = [
            name for name in os.listdir(playthroughs_folder)
            if os.path.isdir(os.path.join(playthroughs_folder, name))
        ]
    else:
        playthrough_names = []

    if request.method == 'POST':
        playthrough_name = request.form['playthrough_name']

        if playthrough_name in playthrough_names:
            session['playthrough_name'] = playthrough_name

            # If turns out that there's a convo ongoing, it shouldn't redirect to choose the participants.
            if os.path.exists(FilesystemManager().get_file_path_to_ongoing_dialogue(playthrough_name)):
                return redirect(url_for('chat'))
            else:
                return redirect(url_for('participants'))
        else:
            return "Invalid playthrough selected.", 400
    else:
        return render_template('index.html', playthrough_names=playthrough_names)


@app.route('/participants', methods=['GET', 'POST'])
def participants():
    playthrough_name = session.get('playthrough_name')
    if not playthrough_name:
        return redirect(url_for('index'))

    characters_manager = CharactersManager(playthrough_name)

    if request.method == 'POST':
        selected_characters = request.form.getlist('selected_characters')
        if len(selected_characters) < 1:
            error = "Please select at least one character."
            # Retrieve character data again for re-rendering the template
            characters = characters_manager.get_characters_at_current_place()

            for character in characters:
                character["image_url"] = url_for("static", filename=character['image_url'])

            return render_template('participants.html', characters=characters, error=error)

        session['participants'] = selected_characters

        return redirect(url_for('chat'))

    # GET request: Retrieve characters at the current place
    characters = characters_manager.get_characters_at_current_place()

    for character in characters:
        character["image_url"] = url_for("static", filename=character['image_url'])

    # After retrieving the characters list
    if not characters:
        message = "There are no characters at your current location."
        return render_template('participants.html', characters=[], message=message)

    return render_template('participants.html', characters=characters)


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    playthrough_name = session.get('playthrough_name')
    dialogue_participants = session.get('participants')

    if not playthrough_name or not dialogue_participants:
        return redirect(url_for('index'))

    if 'dialogue' not in session:
        session['dialogue'] = []

    dialogue = session['dialogue']

    playthrough_manager = PlaythroughManager(playthrough_name)

    player_identifier = playthrough_manager.get_player_identifier()

    participants_instance = Participants()

    if request.method == 'POST':
        user_input = request.form['user_input']

        # Create the observer
        web_dialogue_observer = WebDialogueObserver()

        # Create the player input factory
        web_player_input_factory = WebPlayerInputFactory(user_input)

        SetupDialogueCommand(playthrough_name, player_identifier, participants_instance, web_dialogue_observer,
                             web_player_input_factory,
                             WebMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy(),
                             WebMessageDataProducerForSpeechTurnStrategy(playthrough_name),
                             WebChooseParticipantsStrategy(dialogue_participants)).execute()

        # Get messages from observer and update dialogue
        for message in web_dialogue_observer.get_messages():
            message["sender_photo_url"] = url_for("static", filename=message['sender_photo_url'])
            dialogue.append(message)

        # Remove older messages if the dialogue exceeds the max number of entries
        if len(dialogue) > MAX_DIALOGUE_ENTRIES_FOR_WEB:
            dialogue = dialogue[-MAX_DIALOGUE_ENTRIES_FOR_WEB:]  # Keep only the latest messages

        # Update the dialogue in session
        session['dialogue'] = dialogue

        return redirect(url_for('chat'))
    else:
        return render_template('chat.html', dialogue=dialogue)


if __name__ == '__main__':
    app.run(debug=True)
