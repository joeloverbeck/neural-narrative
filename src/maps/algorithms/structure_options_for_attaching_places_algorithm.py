import logging
from typing import List, Any, Optional

logger = logging.getLogger(__name__)


class StructureOptionsForAttachingPlacesAlgorithm:
    def __init__(
        self,
        items: List[Any],
        value_attr: Optional[str] = None,
        display_attr: Optional[str] = None,
    ):
        self._items = items
        self._value_attr = value_attr
        self._display_attr = display_attr

    def do_algorithm(self) -> list[dict[str, str]]:
        structured = []
        for item in self._items:
            if isinstance(item, dict):
                # If specific attributes are provided, use them; otherwise, default to 'value' and 'display'
                value = (
                    item.get(self._value_attr, "")
                    if self._value_attr
                    else item.get("value", "")
                )
                display = (
                    item.get(self._display_attr, "")
                    if self._display_attr
                    else item.get("display", "")
                )
                logger.info(f"Dict item - Value: {value}, Display: {display}")
            else:
                # Assume the item is a string
                value = item
                display = item
                logger.info(f"String item - Value: {value}, Display: {display}")
            structured.append({"value": value, "display": display})
        return structured
