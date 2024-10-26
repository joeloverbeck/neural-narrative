from flask import render_template, session, redirect, url_for
from flask.views import MethodView


class ActionsView(MethodView):

    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))
        return render_template("actions.html")
