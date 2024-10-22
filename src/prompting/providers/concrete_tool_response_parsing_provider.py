import json
import re
from src.prompting.abstracts.abstract_factories import ToolResponseParsingProvider
from src.prompting.abstracts.factory_products import ToolResponseParsingProduct
from src.prompting.function_call_sanitizer import FunctionCallSanitizer
from src.prompting.products.concrete_tool_response_parsing_product import ConcreteToolResponseParsingProduct


class ConcreteToolResponseParsingProvider(ToolResponseParsingProvider):
    FUNCTION_CALL_STRUCTURE_REGEX = re.compile(
        '<function=(\\w+)>(.*?)</function>', re.DOTALL)

    def __init__(self, response: str):
        if not response:
            raise ValueError('Response cannot be empty')
        self._response = response
        self._function_call_sanitizer = FunctionCallSanitizer(self._response)

    def _clean_json_keys(self, obj):
        if isinstance(obj, dict):
            return {key.strip(): self._clean_json_keys(value) for key,
            value in obj.items()}
        elif isinstance(obj, list):
            return [self._clean_json_keys(item) for item in obj]
        else:
            return obj

    def parse_tool_response(self) -> ToolResponseParsingProduct:
        if not self._response:
            return ConcreteToolResponseParsingProduct(function_json=None,
                                                      is_valid=False, error=
                                                      f'Was tasked to parse the tool call of an empty or invalid response.'
                                                      )
        self._response = self._function_call_sanitizer.sanitize()
        match = re.search(ConcreteToolResponseParsingProvider.
                          FUNCTION_CALL_STRUCTURE_REGEX, self._response)
        if match:
            function_name, args_string = match.groups()
            try:
                args = json.loads(args_string)
                args = self._clean_json_keys(args)
                return ConcreteToolResponseParsingProduct(function_json={
                    'function': function_name, 'arguments': args}, is_valid
                =True, error=None)
            except json.JSONDecodeError as error:
                return ConcreteToolResponseParsingProduct(function_json=
                                                          None, is_valid=False, error=
                                                          f'Error parsing function arguments: {error}. Text: {self._response}'
                                                          )
        return ConcreteToolResponseParsingProduct(function_json=None,
                                                  is_valid=False, error=
                                                  f'Expected a function call from the response, but it was: {self._response}'
                                                  )
