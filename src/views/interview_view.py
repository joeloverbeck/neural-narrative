import logging

from flask import request, session, redirect, url_for, render_template, jsonify
from flask.views import MethodView

from src.base.validators import validate_non_empty_string
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.characters.composers.character_information_provider_factory_composer import (
    CharacterInformationProviderFactoryComposer,
)
from src.interviews.commands.determine_next_interview_question_command import (
    DetermineNextInterviewQuestionCommand,
)
from src.interviews.commands.skip_interview_question_command import (
    SkipInterviewQuestionCommand,
)
from src.interviews.factories.move_to_next_base_question_command_factory import (
    MoveToNextBaseQuestionCommandFactory,
)
from src.interviews.models.interviewee_response import IntervieweeResponse
from src.interviews.providers.interviewee_response_provider import (
    IntervieweeResponseProvider,
)
from src.interviews.repositories.interview_repository import InterviewRepository
from src.interviews.repositories.ongoing_interview_repository import (
    OngoingInterviewRepository,
)
from src.interviews.repositories.questions_repository import QuestionsRepository
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms

logger = logging.getLogger(__name__)


class InterviewView(MethodView):

    @staticmethod
    def _add_interviewee_response(
        playthrough_name: str,
        character_identifier: str,
        character_name: str,
        interviewee_response: str,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(character_name, "character_name")
        validate_non_empty_string(interviewee_response, "interviewee_response")

        ongoing_interview_repository = OngoingInterviewRepository(
            playthrough_name,
            character_identifier,
            character_name,
        )

        # Add interviewee message
        ongoing_interview_repository.add_interviewee_message(interviewee_response)

        # Add the interviewee response to the interview file.
        interview_repository = InterviewRepository(
            playthrough_name, character_identifier, character_name
        )

        interview_repository.add_line(character_name, interviewee_response)

    @staticmethod
    def _add_interviewer_question(
        playthrough_name: str,
        character_identifier: str,
        character_name: str,
        interviewer_question: str,
    ):
        ongoing_interview_repository = OngoingInterviewRepository(
            playthrough_name, character_identifier, character_name
        )

        # Add interviewer message
        ongoing_interview_repository.add_interviewer_message(interviewer_question)

        # Add the line to the interview.
        interview_repository = InterviewRepository(
            playthrough_name, character_identifier, character_name
        )

        interview_repository.add_line("Interviewer", interviewer_question)

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

    def post(self):
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

            if action == "send_next_question":
                # In this action, the user must have sent the next interviewer question, instead of
                # letting the system generate it.
                user_question = request.form.get("user_question")
                if not user_question:
                    return jsonify(
                        {"success": False, "error": "User question cannot be empty"}
                    )

                # We have the user question, so we must set it as the current question of the ongoing interview.
                # However, we must store the existing current question as the last base question, assuming it was
                # actually a base question.
                questions_repository = QuestionsRepository()

                current_interview_question = (
                    ongoing_interview_repository.get_interview_question()
                )

                if questions_repository.is_base_question(current_interview_question):
                    ongoing_interview_repository.set_last_base_question(
                        current_interview_question
                    )

                # Now set the passed question as the current question.
                ongoing_interview_repository.set_interview_question(user_question)

                self._add_interviewer_question(
                    playthrough_name,
                    character_identifier,
                    selected_character.name,
                    user_question,
                )

                response = {
                    "success": True,
                    "message": "User question processed.",
                    "new_message": {
                        "role": "interviewer",
                        "sender": "Interviewer",
                        "content": user_question,
                    },
                }

                return jsonify(response)

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

                self._add_interviewer_question(
                    playthrough_name,
                    character_identifier,
                    selected_character.name,
                    new_question,
                )

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

                self._add_interviewee_response(
                    playthrough_name,
                    character_identifier,
                    selected_character.name,
                    interviewee_response,
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

            elif action == "generate_interviewee_response":
                character_information_provider_factory = (
                    CharacterInformationProviderFactoryComposer(
                        playthrough_name
                    ).compose_factory(character_identifier)
                )

                produce_tool_response_strategy_factory = (
                    ProduceToolResponseStrategyFactoryComposer(
                        Llms().for_interviewee_response()
                    ).compose_factory()
                )

                product = IntervieweeResponseProvider(
                    playthrough_name,
                    character_identifier,
                    selected_character.name,
                    character_information_provider_factory,
                    produce_tool_response_strategy_factory,
                ).generate_product(IntervieweeResponse)

                interviewee_response = product.get()

                self._add_interviewee_response(
                    playthrough_name,
                    character_identifier,
                    selected_character.name,
                    interviewee_response,
                )

                response = {
                    "success": True,
                    "message": f"{selected_character.name}'s response generated.",
                    "new_message": {
                        "role": "interviewee",
                        "sender": selected_character.name,
                        "content": interviewee_response,
                    },
                }

                return jsonify(response)

            elif action == "skip_question":
                SkipInterviewQuestionCommand(
                    playthrough_name, character_identifier, selected_character.name
                ).execute()

                current_interview_question = (
                    ongoing_interview_repository.get_interview_question()
                )

                response = {
                    "success": True,
                    "message": "Question skipped.",
                    "new_message": {
                        "role": "interviewer",
                        "sender": "Interviewer",
                        "content": current_interview_question,
                    },
                }

                return jsonify(response)

        return redirect(url_for("interview"))
