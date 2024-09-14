import logging
from typing import List

from src.characters.characters_manager import CharactersManager

logger = logging.getLogger(__name__)


def gather_participants_data(playthrough_name: str, participants: List[str],
                             characters_manager: CharactersManager = None):
    characters_manager = characters_manager or CharactersManager(playthrough_name)

    participants_data = []  # Initialize an empty list to store participants' data

    for participant in participants:
        try:
            # Load character data for each participant
            character_data = characters_manager.load_character_data(playthrough_name, participant)

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
            logger.error(f"Error loading data for participant {participant}: {e}")

    return participants_data
