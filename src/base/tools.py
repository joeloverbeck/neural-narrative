import json
import logging
import traceback

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
