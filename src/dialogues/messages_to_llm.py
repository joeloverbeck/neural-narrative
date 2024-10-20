from typing import List

from src.base.required_string import RequiredString


class MessagesToLlm:
    def __init__(self):
        self._messages: List[dict] = []
        self._guiding_message_indices: List[int] = []

    def add_message(
            self,
            role: RequiredString,
            content: RequiredString,
            is_guiding_message: bool = False,
    ):
        if not isinstance(role, RequiredString):
            raise TypeError(
                f"At this point, 'role' should be of type RequiredString, but it was '{type(role)}'."
            )
        if not isinstance(content, RequiredString):
            raise TypeError(
                f"At this point, 'content' should be of type RequiredString, but it was '{type(content)}'."
            )

        dict_to_add = {"role": role.value, "content": content.value}

        # If the role is 'system', replace the first message or add it to the beginning
        if role.value == "system":
            if self._messages and self._messages[0]["role"] == "system":
                self._messages[0] = dict_to_add
            else:
                self._messages.insert(0, dict_to_add)
        else:
            self._messages.append(dict_to_add)
            if is_guiding_message:
                # Must add to 'guiding_messages' the index of this last added message,
                # so they're considered special messages.
                latest_entry_index = len(self._messages) - 1
                self._guiding_message_indices.append(latest_entry_index)

    def extend_from_messages_to_llm(self, origin_messages_to_llm: "MessagesToLlm"):
        # Check if there are any 'user' or 'assistant' messages in the current messages
        has_user_or_assistant_message = any(
            msg["role"] in ["assistant", "user"] for msg in self._messages
        )

        # If there are 'user' or 'assistant' messages, skip guiding messages from the origin
        for i, msg in enumerate(origin_messages_to_llm.get()):
            if (
                    has_user_or_assistant_message
                    and i in origin_messages_to_llm.get_guiding_message_indices()
            ):
                # Skip guiding messages
                continue
            else:
                # Add the message to the current list
                self.add_message(msg["role"], msg["content"])

    def get(self) -> List[dict]:
        return self._messages

    def get_guiding_message_indices(self) -> List[int]:
        return self._guiding_message_indices
