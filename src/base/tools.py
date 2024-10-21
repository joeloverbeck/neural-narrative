import json
import logging
import traceback

from src.base.required_string import RequiredString

logger = logging.getLogger(__name__)


def generate_tool_prompt(
    tool: dict, tool_instructions_template: RequiredString
) -> RequiredString:
    return RequiredString(
        tool_instructions_template.value.format(
            tool_name=tool["function"]["name"],
            tool_description=tool["function"]["description"],
            tool=json.dumps(tool["function"]),
        )
    )


def capture_traceback():
    # Capture the full traceback as a string
    tb = traceback.format_exc()

    # Log the traceback with the error ID
    logger.error(f"{tb}")
