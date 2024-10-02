from flask import render_template, request, session, redirect, url_for
from flask.views import MethodView

from src.filesystem.filesystem_manager import FilesystemManager
from src.playthrough_manager import PlaythroughManager


class IndexView(MethodView):

    def get(self):
        filesystem_manager = FilesystemManager()

        # Retrieve the list of existing playthrough folders
        playthrough_names = filesystem_manager.get_playthrough_names()

        # Pop session variables that should be reset now.
        session.pop("no_available_templates", None)

        return render_template("index.html", playthrough_names=playthrough_names)

    def post(self):
        filesystem_manager = FilesystemManager()

        playthrough_name = request.form["playthrough_name"]

        if filesystem_manager.playthrough_exists(playthrough_name):
            session["playthrough_name"] = playthrough_name

            playthrough_manager = PlaythroughManager(playthrough_name)

            # If turns out that there's a convo ongoing, it shouldn't redirect to choose the participants.
            if playthrough_manager.has_ongoing_dialogue(playthrough_name):
                return redirect(url_for("chat"))
            else:
                return redirect(url_for("location-hub"))
        else:
            return "Invalid playthrough selected.", 400
