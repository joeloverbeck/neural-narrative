import json
import re

from src.prompting.abstracts.abstract_factories import ToolResponseParsingFactory
from src.prompting.abstracts.factory_products import ToolResponseParsingProduct
from src.prompting.products.concrete_tool_response_parsing_product import ConcreteToolResponseParsingProduct


class ConcreteToolResponseParsingFactory(ToolResponseParsingFactory):
    def __init__(self, response: str):
        assert response

        self._response = response

    def _fix_tool_call(self):
        # Step 1: Remove leading/trailing spaces and newlines
        self._response = self._response.strip()

        # Step 2: Remove all line breaks within the string
        self._response = self._response.replace("\n", "").replace("\r", "")

        # Step 3: Optionally, remove extra spaces between the tags if needed
        self._response = re.sub(r"\s*<function", "<function", self._response)
        self._response = re.sub(r"</function>\s*", "</function>", self._response)

        # Step 4: Fix the case where the tool call ends with '}}<function>' instead of '}</function>'
        if self._response.endswith('"}}<function>'):
            # Replace with the correct ending
            self._response = self._response.replace('"}}<function>', '}</function>')

        # Step 5: Ensure that the closing tag starts with '<'
        if self._response.endswith('/function>') and not self._response.endswith('</function>'):
            # Add the missing '<' to the closing tag
            self._response = self._response[:-10] + '</function>'

    def _clean_json_keys(self, obj):
        if isinstance(obj, dict):
            # Iterate through the dictionary and clean keys
            return {key.strip(): self._clean_json_keys(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            # If it's a list, apply cleaning recursively to all list items
            return [self._clean_json_keys(item) for item in obj]
        else:
            # If it's not a dictionary or list, return the object itself
            return obj

    def parse_tool_response(self) -> ToolResponseParsingProduct:

        # it could be that the response is almost correct, but the AI has hallucinated something. In that case, the
        # response should be corrected:
        self._fix_tool_call()

        function_regex = r"<function=(\w+)>(.*?)</function>"
        match = re.search(function_regex, self._response)

        if match:
            function_name, args_string = match.groups()
            try:
                args = json.loads(args_string)

                # Clean the arguments' keys by trimming spaces
                args = self._clean_json_keys(args)

                return ConcreteToolResponseParsingProduct(function_json={"function": function_name,
                                                                         "arguments": args, }, is_valid=True,
                                                          error=None)
            except json.JSONDecodeError as error:
                return ConcreteToolResponseParsingProduct(function_json=None, is_valid=False,
                                                          error=f"Error parsing function arguments: {error}. Text: {self._response}")

        return ConcreteToolResponseParsingProduct(function_json=None, is_valid=False,
                                                  error=f"Expected a function call from the response, but it was: {self._response}")
