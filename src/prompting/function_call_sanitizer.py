import re


class FunctionCallSanitizer:
    REMOVE_EXTRA_SPACES_BETWEEN_FUNCTION_TAGS_ONE_REGEX = re.compile(r"\s*<function")
    REMOVE_EXTRA_SPACES_BETWEEN_FUNCTION_TAGS_TWO_REGEX = re.compile(r"</function>\s*")
    REMOVE_EXTRA_CLOSING_BRACES_BEFORE_CLOSING_FUNCTION_TAG_REGEX = re.compile(
        r"}+</function>"
    )
    REMOVE_SPACES_BETWEEN_SYMBOL_OF_FUNCTION_TAG_AND_SYMBOL_OF_JSON_OBJECT_REGEX = (
        re.compile(r">\s+{")
    )
    REMOVE_SPACES_BETWEEN_THE_CLOSING_FUNCTION_TAG_REGEX = re.compile(r"\s+</function>")
    REPLACE_SINGLE_QUOTES_WITH_DOUBLE_QUOTES_REGEX = re.compile(
        r"(?<=[:\[{,])\s*'([^']*)'\s*(?=[,}\]])"
    )
    INSERT_LINE_BREAK_AFTER_PERIOD_WITH_NO_SPACE_FOLLOWED_BY_LETTER_REGEX = re.compile(
        r"\.(?=\w)"
    )
    REMOVE_ANY_EXTRA_SYMBOLS_BETWEEN_JSON_OBJECT_AND_FUNCTION_TAG = re.compile(
        r"}\s*>\s*</function>"
    )
    REPLACE_INCORRECT_CLOSING_FUNCTION_TAG_REGEX = re.compile(r"{/function}")
    REMOVE_EXTRA_CHARACTERS_AFTER_JSON_REGEX = re.compile(r"(}.*?)(</function>)")

    def __init__(self, function_call: str):
        if not function_call:
            raise ValueError("function_call can't be empty or None.")

        self._function_call = function_call

    def sanitize(self) -> str:
        """
        Sanitize the tool call response by performing the following steps:
        1. Strip leading/trailing spaces and newlines.
        2. Remove all line breaks within the string.
        3. Fix formatting issues with function tags and JSON structure.
        """
        function_call = (
            self._function_call.strip()
        )  # Step 1: Remove leading/trailing spaces and newlines
        function_call = function_call.replace("\n", "").replace(
            "\r", ""
        )  # Step 2: Remove all line breaks

        # Step 3: Optionally, remove extra spaces between the function tags if needed
        function_call = re.sub(
            FunctionCallSanitizer.REMOVE_EXTRA_SPACES_BETWEEN_FUNCTION_TAGS_ONE_REGEX,
            "<function",
            function_call,
        )
        function_call = re.sub(
            FunctionCallSanitizer.REMOVE_EXTRA_SPACES_BETWEEN_FUNCTION_TAGS_TWO_REGEX,
            "</function>",
            function_call,
        )

        # Step 4: Fix the case where the tool call ends with '}}<function>' instead of '}</function>'
        function_call = function_call.replace('"}}<function>', "}</function>")

        # Step 5: Ensure the closing tag starts with '<'
        if function_call.endswith("/function>") and not function_call.endswith(
            "</function>"
        ):
            function_call = function_call[:-10] + "</function>"

        # Step 6: Remove extra closing braces before the closing </function> tag
        function_call = re.sub(
            FunctionCallSanitizer.REMOVE_EXTRA_CLOSING_BRACES_BEFORE_CLOSING_FUNCTION_TAG_REGEX,
            "}</function>",
            function_call,
        )

        # Step 7: Remove spaces between '>' of function tag and '{' of JSON object
        function_call = re.sub(
            FunctionCallSanitizer.REMOVE_SPACES_BETWEEN_SYMBOL_OF_FUNCTION_TAG_AND_SYMBOL_OF_JSON_OBJECT_REGEX,
            ">{",
            function_call,
        )

        # Step 8: Remove spaces before the closing </function> tag
        function_call = re.sub(
            FunctionCallSanitizer.REMOVE_SPACES_BETWEEN_THE_CLOSING_FUNCTION_TAG_REGEX,
            "</function>",
            function_call,
        )

        # Step 9: Replace single quotes with double quotes in the JSON part of the response
        # This only targets single quotes around values inside JSON-like structures, avoiding outside content.
        function_call = re.sub(
            FunctionCallSanitizer.REPLACE_SINGLE_QUOTES_WITH_DOUBLE_QUOTES_REGEX,
            r'"\1"',
            function_call,
        )

        # Step 10: Insert a line break after periods with no space followed by a letter
        function_call = re.sub(
            FunctionCallSanitizer.INSERT_LINE_BREAK_AFTER_PERIOD_WITH_NO_SPACE_FOLLOWED_BY_LETTER_REGEX,
            ".\n",
            function_call,
        )

        # Step 11: Replace literal newlines with the escaped version
        function_call = function_call.replace("\n", "\\n").replace("\t", "\\t")

        # Step 12: Remove any extra '>' characters between the JSON object and '</function>' tag
        function_call = re.sub(
            FunctionCallSanitizer.REMOVE_ANY_EXTRA_SYMBOLS_BETWEEN_JSON_OBJECT_AND_FUNCTION_TAG,
            "}</function>",
            function_call,
        )

        # Step 13: Replace incorrect closing function tags '{/function}' with '</function>'
        function_call = re.sub(
            FunctionCallSanitizer.REPLACE_INCORRECT_CLOSING_FUNCTION_TAG_REGEX,
            "</function>",
            function_call,
        )

        # Step 14: Remove any extra characters after the JSON object before the closing </function> tag
        function_call = re.sub(
            FunctionCallSanitizer.REMOVE_EXTRA_CHARACTERS_AFTER_JSON_REGEX,
            r"}\2",
            function_call,
        )

        return function_call
