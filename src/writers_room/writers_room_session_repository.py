from typing import Optional, Dict, Any, List

from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import read_json_file, write_json_file
from src.filesystem.path_manager import PathManager
from src.writers_room.enums import AgentType


class WritersRoomSessionRepository:
    def __init__(self, playthrough_name, path_manager: Optional[PathManager] = None):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

        self._path_manager = path_manager or PathManager()

        self._session_path = self._path_manager.get_writers_room_session(
            playthrough_name
        )
        self._session_data = self._load_session_file()

    def _load_session_file(self) -> Dict[str, Any]:
        return read_json_file(self._session_path)

    def get_messages(self) -> List[Dict[str, str]]:
        return self._session_data.get("messages", [])

    def set_messages(self, messages) -> None:
        self._session_data["messages"] = messages

    def get_agent_name(self) -> str:
        return self._session_data.get("agent_name", AgentType.SHOWRUNNER.value)

    def set_agent_name(self, agent_name) -> None:
        validate_non_empty_string(agent_name, "agent_name")

        self._session_data["agent_name"] = agent_name

    def get_context_variables(self) -> Dict[str, Any]:
        return self._session_data.get("context_variables", {})

    def set_context_variables(self, context_variables: Dict[str, Any]) -> None:
        self._session_data["context_variables"] = context_variables

    def save(self) -> None:
        write_json_file(self._session_path, self._session_data)
