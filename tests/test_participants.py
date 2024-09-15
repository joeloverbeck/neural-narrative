from src.dialogues.participants import Participants


def test_add_existing_participant():
    # Create a Participants instance
    participants = Participants()

    # Add two participants
    participants.add_participant("1", "Alice", "description", "friendly", "equipment")
    participants.add_participant("2", "Bob", "description", "serious", "equipment")

    # Capture the original state of the keys in _participants
    original_keys = set(participants._participants.keys())

    # Add a participant with an existing identifier (id1)
    participants.add_participant("1", "Alice", "description", "friendly but competitive", "equipment")

    # Ensure that the original keys have not been modified
    assert original_keys == set(participants._participants.keys()), \
        "Keys in _participants should not change when adding a participant with an existing identifier."


def test_add_new_participant():
    # Create a Participants instance
    participants = Participants()

    # Add a participant
    participants.add_participant("1", "Alice", "description", "friendly", "equipment")

    # Capture the original state of the keys
    original_keys = set(participants._participants.keys())

    # Add a new participant with a different identifier
    participants.add_participant("2", "Bob", "description", "serious", "equipment")

    # Ensure that the keys have been updated correctly
    assert original_keys != set(participants._participants.keys()), \
        "Keys in _participants should be updated when adding a new participant."
    assert "2" in participants._participants, "New participant key '2' should be present."
