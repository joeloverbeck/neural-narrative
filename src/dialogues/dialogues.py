from typing import List

from src.characters.characters import load_character_data
from src.dialogues.abstracts.factory_products import SpeechDataProduct


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
                'description': character_data.get('description'),
                'personality': character_data.get('personality'),
                'equipment': character_data.get('equipment')
            }

            # Append the participant's info to the list
            participants_data.append(participant_info)

        except (FileNotFoundError, KeyError) as e:
            print(f"Error loading data for participant {participant}: {e}")

    return participants_data


def compose_speech_entry(speech_data_product: SpeechDataProduct):
    return f"{speech_data_product.get()["name"]}: *{speech_data_product.get()['narration_text']}* {speech_data_product.get()['speech']}"
