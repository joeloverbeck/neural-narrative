import ast
import json
import re

from src.base.validators import validate_non_empty_string


class FunctionCallSanitizer:
    (INSERT_LINE_BREAK_AFTER_PERIOD_WITH_NO_SPACE_FOLLOWED_BY_LETTER_REGEX) = (
        re.compile("\\.(?=[A-Z])")
    )
    REPLACE_INCORRECT_CLOSING_FUNCTION_TAG_REGEX = re.compile("\\[/function]")
    REMOVE_EXTRA_CHARACTERS_AFTER_JSON_REGEX = re.compile("(}.*?)(</function>)")
    FIX_CLOSING_FUNCTION_TAG_WITHOUT_LT_OR_SLASH = re.compile(
        "(?<!<)(?<!</)(?<!\\w)function>"
    )
    REPLACE_SELF_CLOSING_FUNCTION_TAG_AT_END_REGEX = re.compile("<function\\s*/>\\s*$")
    REPLACE_INCORRECT_CLOSING_FUNCTION_TAG_AT_END_REGEX = re.compile(
        "}\\s*<function>\\s*$"
    )
    REPLACE_START_TAG_PLACEHOLDER_REGEX = re.compile("<\\{start_tag}=(.*?)>")
    REMOVE_END_TAG_PLACEHOLDER_REGEX = re.compile("</end_tag>")

    def __init__(self, function_call: str):
        validate_non_empty_string(function_call, "function_call")
        self._function_call = function_call

    @staticmethod
    def _insert_newline_after_period_followed_by_uppercase(s):
        return re.sub("\\.([A-Z])", ".\\n\\1", s)

    def _process_data(self, data):
        if isinstance(data, dict):
            return {k: self._process_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._process_data(v) for v in data]
        elif isinstance(data, str):
            return self._insert_newline_after_period_followed_by_uppercase(data)
        else:
            return data

    def _fix_single_quoted_list_items(self, function_call: str) -> str:
        function_tag_regex = "<function(?:=|\\s+name=)([^\\s>]+)>(.*?)</function>"
        match = re.search(function_tag_regex, function_call)
        if not match:
            return function_call
        function_name = match.group(1)
        json_content = match.group(2)
        try:
            data = ast.literal_eval(json_content)
            data = self._process_data(data)
            json_str = json.dumps(data)
        except Exception:
            return function_call
        sanitized_function_call = f"<function={function_name}>{json_str}</function>"
        return sanitized_function_call

    def sanitize(self) -> str:
        """
        Sanitize the tool call response by performing the following steps:
        1. Strip leading/trailing spaces and newlines.
        2. Remove all line breaks within the string.
        3. Fix formatting issues with function tags and JSON structure.
        """
        function_call = (
            self._function_call.strip()
            .replace("\n", "")
            .replace("\r", "")
            .replace("}<>", "}")
        )
        function_call = re.sub(
            FunctionCallSanitizer.REPLACE_START_TAG_PLACEHOLDER_REGEX,
            "<function=\\1>",
            function_call,
        )
        function_call = re.sub(
            FunctionCallSanitizer.REMOVE_END_TAG_PLACEHOLDER_REGEX, "", function_call
        )
        function_call = re.sub(
            FunctionCallSanitizer.REPLACE_INCORRECT_CLOSING_FUNCTION_TAG_REGEX,
            "</function>",
            function_call,
        )
        function_call = re.sub(
            FunctionCallSanitizer.FIX_CLOSING_FUNCTION_TAG_WITHOUT_LT_OR_SLASH,
            "</function>",
            function_call,
        )
        function_call = re.sub(
            FunctionCallSanitizer.REMOVE_EXTRA_CHARACTERS_AFTER_JSON_REGEX,
            "}\\2",
            function_call,
        )
        function_call = re.sub(
            FunctionCallSanitizer.REPLACE_SELF_CLOSING_FUNCTION_TAG_AT_END_REGEX,
            "</function>",
            function_call,
        )
        function_call = re.sub(
            FunctionCallSanitizer.REPLACE_INCORRECT_CLOSING_FUNCTION_TAG_AT_END_REGEX,
            "}</function>",
            function_call,
        )
        function_call = self._fix_single_quoted_list_items(function_call)
        if not function_call.endswith("</function>"):
            function_call += "</function>"
        return function_call
