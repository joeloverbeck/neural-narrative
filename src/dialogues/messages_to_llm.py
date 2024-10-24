from typing import List


class MessagesToLlm:

    def __init__(self):
        self._messages: List[dict] = []
        self._guiding_message_indices: List[int] = []

    def add_message(self, role: str, content: str, is_guiding_message: bool = False):
        dict_to_add = {"role": role, "content": content}
        if role == "system":
            if self._messages and self._messages[0]["role"] == "system":
                self._messages[0] = dict_to_add
            else:
                self._messages.insert(0, dict_to_add)
        else:
            self._messages.append(dict_to_add)
            if is_guiding_message:
                latest_entry_index = len(self._messages) - 1
                self._guiding_message_indices.append(latest_entry_index)

    def get(self) -> List[dict]:
        return self._messages

    def get_guiding_message_indices(self) -> List[int]:
        return self._guiding_message_indices
