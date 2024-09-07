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

        # Check if the tool call ends with the incorrect ending
        if self._response.endswith('"}}<function>'):
            # Replace with the correct ending
            self._response = self._response.replace('"}}<function>', '}</function>')

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
                return ConcreteToolResponseParsingProduct(function_json={"function": function_name,
                                                                         "arguments": args, }, is_valid=True,
                                                          error=None)
            except json.JSONDecodeError as error:
                return ConcreteToolResponseParsingProduct(function_json=None, is_valid=False,
                                                          error=f"Error parsing function arguments: {error}")

        return ConcreteToolResponseParsingProduct(function_json=None, is_valid=False,
                                                  error=f"Expected a function call from the response, but it was: {self._response}")
