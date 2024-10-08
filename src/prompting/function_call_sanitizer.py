import ast
import json
import re


class FunctionCallSanitizer:
    INSERT_LINE_BREAK_AFTER_PERIOD_WITH_NO_SPACE_FOLLOWED_BY_LETTER_REGEX = re.compile(
        r"\.(?=\w)"
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

    def __init__(self, function_call: str):
        if not function_call:
            raise ValueError("function_call can't be empty or None.")

        self._function_call = function_call

    @staticmethod
    def _fix_single_quoted_list_items(function_call: str) -> str:
        function_tag_regex = r"<function(?:=|\s+name=)([^\s>]+)>(.*?)</function>"
        match = re.match(function_tag_regex, function_call)
        if not match:
            # If no match, return the original function_call
            return function_call

        function_name = match.group(1)
        json_content = match.group(2)

        # Step 4: Attempt to parse the JSON-like content using ast.literal_eval
        try:
            data = ast.literal_eval(json_content)
            # Step 5: Serialize back to JSON string with proper formatting
            json_str = json.dumps(data)
        except Exception:
            # If parsing fails, return the original function_call
            return function_call

        # Step 6: Reconstruct the sanitized function call
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
        )  # Remove leading/trailing spaces and newlines
        function_call = function_call.replace("\n", "").replace(
            "\r", ""
        )  # Remove all line breaks

        # Insert a line break after periods with no space followed by a letter
        function_call = re.sub(
            FunctionCallSanitizer.INSERT_LINE_BREAK_AFTER_PERIOD_WITH_NO_SPACE_FOLLOWED_BY_LETTER_REGEX,
            ".\n",
            function_call,
        )

        # Replace literal newlines with the escaped version
        function_call = function_call.replace("\n", "\\n").replace("\t", "\\t")

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

        # Step 20: Ensure that the function call ends with '</function>'
        if not function_call.endswith("</function>"):
            function_call += "</function>"

        return function_call
