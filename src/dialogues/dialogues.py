from typing import List, Any

from src.characters.characters import load_character_data
from src.characters.commands.store_character_memory import StoreCharacterMemory
from src.constants import HERMES_405B, \
    SUMMARIZE_DIALOGUE_PROMPT_FILE, DIALOGUE_SUMMARIZATION_TOOL_FILE, TOOL_INSTRUCTIONS_FILE
from src.files import read_file, read_json_file
from src.prompting.factories.concrete_tool_response_parsing_factory import ConcreteToolResponseParsingFactory
from src.prompting.factories.dialogue_summary_tool_response_data_extraction_factory import \
    DialogueSummaryToolResponseDataExtractionFactory
from src.prompting.factories.open_ai_llm_content_factory import OpenAiLlmContentFactory
from src.tools import generate_tool_prompt


def gather_participant_data(playthrough_name: str, participants: List[int]):
    participants_data = []  # Initialize an empty list to store participants' data

    for participant in participants:
        try:
            # Load character data for each participant
            character_data = load_character_data(playthrough_name, participant)

            # Assuming the character data has a 'name' field
            participant_info = {
                'identifier': participant,
                'name': character_data.get('name', 'Unknown'),
                'description': character_data.get('description')
            }

            # Append the participant's info to the list
            participants_data.append(participant_info)

        except (FileNotFoundError, KeyError) as e:
            print(f"Error loading data for participant {participant}: {e}")

    return participants_data


def summarize_dialogue(playthrough_name, client, participants: List[int], dialogue: List[dict[Any, str]]):
    assert len(participants) >= 2

    # Once the chat is over, the LLM should be prompted to create a memory out of it for all participants.
    if not dialogue or len(dialogue) <= 4:
        # Perhaps the dialogue is empty. In that case, no summary needs to be done.
        print("Won't create memories out of an empty dialogue or insufficient dialogue.")
        return

    system_content = read_file(
        SUMMARIZE_DIALOGUE_PROMPT_FILE) + f"\n\nHere's the dialogue to summarize:\n{dialogue}" + generate_tool_prompt(
        read_json_file(DIALOGUE_SUMMARIZATION_TOOL_FILE), read_file(TOOL_INSTRUCTIONS_FILE))

    messages = [
        {
            "role": "system",
            "content": system_content,
        },
        {
            "role": "user",
            "content": "Summarize the provided dialogue."
        }
    ]

    # Now prompt the LLM for a response.
    llm_content_product = OpenAiLlmContentFactory(client=client, model=HERMES_405B,
                                                  messages=messages).generate_content()

    if llm_content_product.is_valid():
        tool_response_parsing_product = ConcreteToolResponseParsingFactory(
            llm_content_product.get()).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            raise ValueError(
                f"Failed to parse the tool response from the LLM: {tool_response_parsing_product.get_error()}")

        summary = DialogueSummaryToolResponseDataExtractionFactory(
            tool_response_parsing_product.get()).extract_data().get()

        # Now that we have the summary, gotta add it to the memories of all participants.
        for participant_identifier in participants:
            StoreCharacterMemory(playthrough_name, participant_identifier, summary).execute()
    else:
        raise ValueError(f"Failed to summarize dialogue: {llm_content_product.get_error()}")
