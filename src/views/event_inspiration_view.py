import os

from flask import session, redirect, url_for, render_template, request
from flask.views import MethodView

from src.filesystem.filesystem_manager import FilesystemManager


class EventInspirationView(MethodView):
    def get(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        filesystem_manager = FilesystemManager()

        # Get file paths
        situations_file_path = (
            filesystem_manager.get_file_path_to_interesting_situations(playthrough_name)
        )
        dilemmas_file_path = filesystem_manager.get_file_path_to_interesting_dilemmas(
            playthrough_name
        )

        # Initialize lists
        interesting_situations = []
        interesting_dilemmas = []

        # Read situations
        if os.path.exists(situations_file_path):
            situations_content = filesystem_manager.read_file(situations_file_path)
            interesting_situations = [
                line.strip()
                for line in situations_content.strip().split("\n")
                if line.strip()
            ]

        # Read dilemmas
        if os.path.exists(dilemmas_file_path):
            dilemmas_content = filesystem_manager.read_file(dilemmas_file_path)
            interesting_dilemmas = [
                line.strip()
                for line in dilemmas_content.strip().split("\n")
                if line.strip()
            ]

        return render_template(
            "event-inspiration.html",
            interesting_situations=interesting_situations,
            interesting_dilemmas=interesting_dilemmas,
        )

    def post(self):
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        action = request.form.get("action")
        filesystem_manager = FilesystemManager()

        if action == "remove_situation":
            index = int(request.form.get("situation_index"))
            filesystem_manager.remove_item_from_file(
                filesystem_manager.get_file_path_to_interesting_situations(
                    playthrough_name
                ),
                index,
            )
        elif action == "remove_dilemma":
            index = int(request.form.get("dilemma_index"))
            filesystem_manager.remove_item_from_file(
                filesystem_manager.get_file_path_to_interesting_dilemmas(
                    playthrough_name
                ),
                index,
            )

        return redirect(url_for("event-inspiration"))
