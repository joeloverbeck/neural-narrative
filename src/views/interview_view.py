import logging

from flask import request, session, redirect, url_for, render_template, jsonify
from flask.views import MethodView

from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.interviews.commands.determine_next_interview_question_command import (
    DetermineNextInterviewQuestionCommand,
)
from src.interviews.factories.move_to_next_base_question_command_factory import (
    MoveToNextBaseQuestionCommandFactory,
)
from src.interviews.repositories.interview_repository import InterviewRepository
from src.interviews.repositories.ongoing_interview_repository import (
    OngoingInterviewRepository,
)

logger = logging.getLogger(__name__)


class InterviewView(MethodView):

    @staticmethod
    def get():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        characters_manager = CharactersManager(playthrough_name)
        all_characters = characters_manager.get_all_characters()
        selected_character_identifier = request.args.get("character_identifier")
        selected_character = None

        messages = []
        last_message_role = None

        if selected_character_identifier:
            selected_character = Character(
                playthrough_name, selected_character_identifier
            )

            # Load messages from OngoingInterviewRepository
            ongoing_interview_repository = OngoingInterviewRepository(
                playthrough_name,
                selected_character_identifier,
                selected_character.name,
            )

            messages_data = ongoing_interview_repository.get_messages()

            # Process messages_data to format it for template
            messages = []
            for message in messages_data:
                role = (
                    "interviewer" if message["name"] == "interviewer" else "interviewee"
                )
                messages.append(
                    {
                        "role": role,
                        "sender": message["name"],
                        "content": message["message"],
                    }
                )

            if messages:
                last_message_role = messages[-1]["role"]
            else:
                last_message_role = (
                    "interviewee"  # Default to show generate question button
                )

        for character in all_characters:
            character["selected"] = False
            if (
                selected_character
                and character["identifier"] == character["identifier"]
            ):
                character["selected"] = True

        return render_template(
            "interview.html",
            all_characters=all_characters,
            selected_character=selected_character,
            messages=messages,
            last_message_role=last_message_role,
        )

    @staticmethod
    def post():
        playthrough_name = session.get("playthrough_name")
        if not playthrough_name:
            return redirect(url_for("index"))

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            action = request.form.get("submit_action")
            character_identifier = request.form.get("character_identifier")
            if not character_identifier:
                return jsonify({"success": False, "error": "Character not selected"})

            selected_character = Character(playthrough_name, character_identifier)

            ongoing_interview_repository = OngoingInterviewRepository(
                playthrough_name,
                character_identifier,
                selected_character.name,
            )

            if action == "generate_next_question":
                # Determine the next interview question
                move_to_next_base_question_command_factory = (
                    MoveToNextBaseQuestionCommandFactory(
                        playthrough_name, character_identifier, selected_character.name
                    )
                )

                determine_next_question_command = DetermineNextInterviewQuestionCommand(
                    playthrough_name,
                    character_identifier,
                    selected_character.name,
                    move_to_next_base_question_command_factory,
                )

                determine_next_question_command.execute()

                new_question = ongoing_interview_repository.get_interview_question()

                # Add interviewer message
                ongoing_interview_repository.add_interviewer_message(new_question)

                # Add the line to the interview.
                interview_repository = InterviewRepository(
                    playthrough_name, character_identifier, selected_character.name
                )

                interview_repository.add_line("Interviewer", new_question)

                response = {
                    "success": True,
                    "message": "Next question generated.",
                    "new_message": {
                        "role": "interviewer",
                        "sender": "Interviewer",
                        "content": new_question,
                    },
                }

                return jsonify(response)

            elif action == "send_interviewee_response":
                interviewee_response = request.form.get("interviewee_response", "")
                if not interviewee_response:
                    return jsonify(
                        {"success": False, "error": "Response cannot be empty"}
                    )

                # Add interviewee message
                ongoing_interview_repository.add_interviewee_message(
                    interviewee_response
                )

                # Add the interviewee response to the interview file.
                interview_repository = InterviewRepository(
                    playthrough_name, character_identifier, selected_character.name
                )

                interview_repository.add_line(
                    selected_character.name, interviewee_response
                )

                response = {
                    "success": True,
                    "message": "Response sent.",
                    "new_message": {
                        "role": "interviewee",
                        "sender": selected_character.name,
                        "content": interviewee_response,
                    },
                }

                return jsonify(response)

        return redirect(url_for("interview"))
