import json
import re

from src.prompting.abstracts.abstract_factories import ToolResponseParsingFactory
from src.prompting.abstracts.factory_products import ToolResponseParsingProduct
from src.prompting.products.concrete_tool_response_parsing_product import ConcreteToolResponseParsingProduct


class ConcreteToolResponseParsingFactory(ToolResponseParsingFactory):
    def __init__(self, response: str):
        assert response

        self._response = response

    def parse_tool_response(self) -> ToolResponseParsingProduct:
        # "response" shouldn't be empty or None at this point

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
