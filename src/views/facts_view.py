import logging

from flask import session, redirect, url_for, render_template, request, jsonify
from flask.views import MethodView

from src.base.tools import capture_traceback
from src.databases.chroma_db_database import ChromaDbDatabase
from src.interfaces.web_interface_manager import WebInterfaceManager

logger = logging.getLogger(__name__)


class FactsView(MethodView):

    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        return render_template("facts.html")

    @staticmethod
    def post():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        action = request.form.get("submit_action")

        if action == "insert_fact":
            fact = request.form.get("fact", "")
            fact = WebInterfaceManager.remove_excessive_newline_characters(fact)

            facts = fact.splitlines()

            if not facts:
                response = {
                    "success": False,
                    "error": "No fact to save.",
                }
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(response)
                else:
                    return redirect(url_for("facts"))
            try:
                database = ChromaDbDatabase(playthrough_name)

                logger.info("Facts to add: %s", facts)

                [database.insert_fact(fact) for fact in facts if fact]

                response = {
                    "success": True,
                    "message": "Fact saved.",
                }
            except Exception as e:
                response = {
                    "success": False,
                    "error": f"Unable to save fact. Error: {str(e)}",
                }

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
            else:
                return redirect(url_for("facts"))
        elif action == "query_facts":
            query_text = request.form.get("query", "")
            top_k = request.form.get("top_k", 5)

            try:
                top_k = int(top_k)
            except ValueError:
                top_k = 5

            if not query_text.strip():
                response = {
                    "success": False,
                    "error": "Please enter a query.",
                }
                return jsonify(response)

            try:
                database = ChromaDbDatabase(playthrough_name)
                facts = database.retrieve_facts(query_text, top_k=top_k)
                response = {
                    "success": True,
                    "message": "Query successful.",
                    "results": facts,
                }
            except Exception as e:
                capture_traceback()
                response = {
                    "success": False,
                    "error": f"Unable to retrieve facts. Error: {str(e)}",
                }

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(response)
            else:
                return redirect(url_for("facts"))
        return redirect(url_for("facts"))
