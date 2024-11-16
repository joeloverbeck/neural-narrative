import json
import logging
import traceback
from typing import Any

logger = logging.getLogger(__name__)


def generate_tool_prompt(tool: dict, tool_instructions_template: str) -> str:
    return tool_instructions_template.format(
        tool_name=tool["function"]["name"],
        tool_description=tool["function"]["description"],
        tool=json.dumps(tool["function"]),
    )


def capture_traceback():
    tb = traceback.format_exc()
    logger.error(f"{tb}")


def join_with_newline(*args: Any) -> str:
    """
    Joins an arbitrary number of arguments with a newline character.

    Args:
        *args: Any number of arguments of any type.

    Returns:
        A single string with each argument separated by a newline.

    Raises:
        ValueError: If no arguments are provided.
    """
    if not args:
        raise ValueError("At least one argument is required to join.")

    string_args = []
    for arg in args:
        if not isinstance(arg, str):
            raise TypeError(f"All arguments must be strings. Invalid argument: {arg}")
        string_args.append(arg)

    return "\n".join(string_args)


def is_convertible_to_int(s):
    try:
        int_value = int(s)
        return True, int_value
    except ValueError:
        return False, None
