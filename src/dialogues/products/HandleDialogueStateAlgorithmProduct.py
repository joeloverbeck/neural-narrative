from typing import Optional, Dict, Any


class HandleDialogueStateAlgorithmProduct:
    def __init__(self, data: Optional[Dict[str, Any]]):
        self._data = data

    def get_data(self) -> Optional[Dict[str, Any]]:
        return self._data
