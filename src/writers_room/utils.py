from src.filesystem.file_operations import (
    create_directories,
    create_empty_file_if_not_exists,
    create_empty_json_file_if_not_exists,
)
from src.filesystem.path_manager import PathManager


def ensure_writers_room_files(playthrough_name):
    """Ensure that the necessary files and directories exist for the writer's room."""
    path_manager = PathManager()

    create_directories(path_manager.get_writers_room_path(playthrough_name))
    create_empty_file_if_not_exists(
        path_manager.get_writers_room_context_path(playthrough_name)
    )
    create_empty_json_file_if_not_exists(
        path_manager.get_writers_room_session(playthrough_name)
    )


def prepare_messages_for_template(messages):
    """Prepare messages data for the template."""
    messages_data = []
    for message in messages:
        message_text = message.get("content", "")
        if message.get("role") == "user":
            message_type = "user"
            sender = "You"
        else:
            message_type = message.get("sender", "assistant")
            sender = message.get("sender", "Assistant")
        messages_data.append(
            {
                "message_text": message_text,
                "message_type": message_type,
                "sender": sender,
                "timestamp": message.get("timestamp"),
            }
        )
    return messages_data
