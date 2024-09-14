import os

from flask import Flask, request, session, redirect, url_for, render_template

from src.characters.characters_manager import CharactersManager
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager

app = Flask(__name__)
app.secret_key = 'neural-narrative'  # Needed for session management

from src.abstracts.observer import Observer


class WebDialogueObserver(Observer):
    def __init__(self):
        self.messages = []

    def update(self, message: dict) -> None:
        # message should contain 'sender_id' and 'content'
        self.messages.append(message)


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

    playthrough_manager = PlaythroughManager(playthrough_name)
    map_manager = MapManager(playthrough_name)
    characters_manager = CharactersManager(playthrough_name)

    if request.method == 'POST':
        selected_characters = request.form.getlist('selected_characters')
        if len(selected_characters) < 1:
            error = "Please select at least one character."
            # Retrieve character data again for re-rendering the template
            characters = characters_manager.get_characters_at_current_place()

            return render_template('participants.html', characters=characters, error=error)
        session['participants'] = selected_characters
        return redirect(url_for('chat'))

    # GET request: Retrieve characters at the current place
    characters = characters_manager.get_characters_at_current_place()

    # After retrieving the characters list
    if not characters:
        message = "There are no characters at your current location."
        return render_template('participants.html', characters=[], message=message)

    return render_template('participants.html', characters=characters)


if __name__ == '__main__':
    app.run(debug=True)
