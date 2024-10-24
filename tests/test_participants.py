import pytest

from src.dialogues.participants import Participants


def test_identifier_not_convertible_to_int():
    # Setup
    participants = Participants()
    # Attempt to add a participant with a non-integer identifier
    with pytest.raises(ValueError) as exc_info:
        participants.add_participant(
            "abc",
            "NPC",
            "NPC Description",
            "NPC Personality",
            "NPC Equipment",
            "NPC Voice Model",
        )

    assert str(exc_info.value) == "identifier must be convertible to an integer."


def test_name_equals_description():
    # Setup
    participants = Participants()
    # Attempt to add a participant with name equal to description
    with pytest.raises(ValueError) as exc_info:
        participants.add_participant(
            "2",
            "Same",
            "Same",
            "Personality",
            "Equipment",
            "Voice Model",
        )

    assert (
        str(exc_info.value)
        == "Attempted to add a participant for whom the name was equal to the description."
    )
