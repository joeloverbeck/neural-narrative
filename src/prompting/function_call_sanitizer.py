import ast
import json
import re


class FunctionCallSanitizer:
    INSERT_LINE_BREAK_AFTER_PERIOD_WITH_NO_SPACE_FOLLOWED_BY_LETTER_REGEX = re.compile(
        r"\.(?=[A-Z])"
    )
    REPLACE_INCORRECT_CLOSING_FUNCTION_TAG_REGEX = re.compile(r"\[/function]")
    REMOVE_EXTRA_CHARACTERS_AFTER_JSON_REGEX = re.compile(r"(}.*?)(</function>)")
    FIX_CLOSING_FUNCTION_TAG_WITHOUT_LT_OR_SLASH = re.compile(
        r"(?<!<)(?<!</)(?<!\w)function>"
    )
    REPLACE_SELF_CLOSING_FUNCTION_TAG_AT_END_REGEX = re.compile(r"<function\s*/>\s*$")
    REPLACE_INCORRECT_CLOSING_FUNCTION_TAG_AT_END_REGEX = re.compile(
        r"}\s*<function>\s*$"
    )
    REPLACE_START_TAG_PLACEHOLDER_REGEX = re.compile(r"<\{start_tag\}=(.*?)>")
    REMOVE_END_TAG_PLACEHOLDER_REGEX = re.compile(r"</end_tag>")

    def __init__(self, function_call: str):
        if not function_call:
            raise ValueError("function_call can't be empty or None.")

        self._function_call = function_call

    @staticmethod
    def _fix_single_quoted_list_items(function_call: str) -> str:
        function_tag_regex = r"<function(?:=|\s+name=)([^\s>]+)>(.*?)</function>"
        match = re.search(function_tag_regex, function_call)
        if not match:
            # If no match, return the original function_call
            return function_call

        function_name = match.group(1)
        json_content = match.group(2)

        # Attempt to parse the JSON-like content using ast.literal_eval
        try:
            data = ast.literal_eval(json_content)

            # Process the data to fix strings
            def insert_newline_after_period_followed_by_uppercase(s):
                return re.sub(r"\.([A-Z])", r".\n\1", s)

            def process_data(data):
                if isinstance(data, dict):
                    return {k: process_data(v) for k, v in data.items()}
                elif isinstance(data, list):
                    return [process_data(v) for v in data]
                elif isinstance(data, str):
                    return insert_newline_after_period_followed_by_uppercase(data)
                else:
                    return data

            data = process_data(data)

            # Serialize back to JSON string with proper formatting
            json_str = json.dumps(data)
        except Exception:
            # If parsing fails, return the original function_call
            return function_call

        # Reconstruct the sanitized function call
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

        # Replace the start tag placeholder with '<function='
        function_call = re.sub(
            FunctionCallSanitizer.REPLACE_START_TAG_PLACEHOLDER_REGEX,
            r"<function=\1>",
            function_call,
        )

        # Remove the end tag placeholder
        function_call = re.sub(
            FunctionCallSanitizer.REMOVE_END_TAG_PLACEHOLDER_REGEX, "", function_call
        )

        # Replace incorrect closing function tags like '[/function]' with '</function>'
        function_call = re.sub(
            FunctionCallSanitizer.REPLACE_INCORRECT_CLOSING_FUNCTION_TAG_REGEX,
            "</function>",
            function_call,
        )

        # Fix closing function tag without proper opening symbols
        function_call = re.sub(
            FunctionCallSanitizer.FIX_CLOSING_FUNCTION_TAG_WITHOUT_LT_OR_SLASH,
            r"</function>",
            function_call,
        )

        # Remove any extra characters after the JSON object before the closing </function> tag
        function_call = re.sub(
            FunctionCallSanitizer.REMOVE_EXTRA_CHARACTERS_AFTER_JSON_REGEX,
            r"}\2",
            function_call,
        )

        # Replace self-closing function tag at the end with proper closing tag '</function>'
        function_call = re.sub(
            FunctionCallSanitizer.REPLACE_SELF_CLOSING_FUNCTION_TAG_AT_END_REGEX,
            "</function>",
            function_call,
        )

        # Replace incorrect closing tag '...}<function>' with '...}</function>'
        function_call = re.sub(
            FunctionCallSanitizer.REPLACE_INCORRECT_CLOSING_FUNCTION_TAG_AT_END_REGEX,
            "}</function>",
            function_call,
        )

        function_call = self._fix_single_quoted_list_items(function_call)

        # Ensure that the function call ends with '</function>'
        if not function_call.endswith("</function>"):
            function_call += "</function>"

        return function_call
