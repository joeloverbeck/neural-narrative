from typing import Optional, Dict, Any

from src.dialogues.enums import HandleDialogueStateAlgorithmResultType


class HandleDialogueStateAlgorithmProduct:
    def __init__(
            self,
            data: Optional[Dict[str, Any]],
            result_type: HandleDialogueStateAlgorithmResultType,
    ):
        self._data = data
        self._result_type = result_type

    def get_data(self) -> Optional[Dict[str, Any]]:
        return self._data

    def get_result_type(self) -> HandleDialogueStateAlgorithmResultType:
        return self._result_type
