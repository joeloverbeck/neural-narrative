import json
from typing import Dict, Any

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


def prepare_tool_calls_text(message: Dict[str, Any]):
    tool_calls = message.get("tool_calls", [])

    tool_calls_text_list = []

    # It could be that there are no tool calls.
    if tool_calls:
        for tool_call in tool_calls:
            f = tool_call["function"]
            name, args = f["name"], f["arguments"]
            arg_str = json.dumps(json.loads(args)).replace(":", "=")
            tool_calls_text_list.append(f"{name} ({arg_str[1:-1]})")

    return "\n".join(tool_calls_text_list)


def prepare_messages(messages):
    messages_data = []

    for message in messages:
        message_text = message.get("content", "")

        message_text = "No content" if not message_text else message_text

        if message.get("role") == "user":
            message_type = "user"
            sender = "You"
        elif message.get("role") == "tool":
            continue
        else:
            message_type = message.get("sender", "assistant")
            sender = message.get("sender", "Assistant")

        messages_data.append(
            {
                "message_text": message_text,
                "message_type": message_type,
                "sender": sender,
                "tool_calls": prepare_tool_calls_text(message),
                "timestamp": message.get("timestamp"),
            }
        )

    return messages_data
