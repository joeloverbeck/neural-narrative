import pytest

from src.prompting.providers.concrete_tool_response_parsing_provider import ConcreteToolResponseParsingProvider


@pytest.mark.parametrize("response, expected_response", [
    ("    <function=test> {\"arg\": 1}  </function>  ", "<function=test>{\"arg\": 1}</function>"),
    ("\n<function=test> {\"arg\": 1}\n</function>\n", "<function=test>{\"arg\": 1}</function>"),
    ("<function=test> {\"arg\": 1}}</function>", "<function=test>{\"arg\": 1}</function>"),
])
def test_fix_tool_call(response, expected_response):
    provider = ConcreteToolResponseParsingProvider(response)
    provider._sanitize_response()
    assert provider._response == expected_response


@pytest.mark.parametrize("input_json, expected_output", [
    ({" key1 ": "value1", " key2 ": {" nested key ": "value2"}}, {"key1": "value1", "key2": {"nested key": "value2"}}),
    ({" key ": [{" nested_key ": "value"}]}, {"key": [{"nested_key": "value"}]})
])
def test_clean_json_keys(input_json, expected_output):
    provider = ConcreteToolResponseParsingProvider("dummy")
    assert provider._clean_json_keys(input_json) == expected_output


@pytest.mark.parametrize("response, expected_function_name, expected_arguments", [
    ('<function=myFunction>{"arg1": "value1", "arg2": 2}</function>', "myFunction", {"arg1": "value1", "arg2": 2}),
    ('<function=otherFunction>{"arg": true}</function>', "otherFunction", {"arg": True}),
])
def test_parse_tool_response_success(response, expected_function_name, expected_arguments):
    provider = ConcreteToolResponseParsingProvider(response)
    product = provider.parse_tool_response()
    assert product.is_valid()
    assert product.get()["function"] == expected_function_name
    assert product.get()["arguments"] == expected_arguments
    assert product.get_error() is None


@pytest.mark.parametrize("response", [
    '<function=myFunction>{"arg1": "value1", "arg2": } </function>',  # Invalid JSON
    '<function=myFunction>{"arg1": "value1"</function>',  # Malformed JSON
])
def test_parse_tool_response_json_error(response):
    provider = ConcreteToolResponseParsingProvider(response)
    product = provider.parse_tool_response()
    assert not product.is_valid()
    assert product.get() is None
    assert "Error parsing function arguments" in product.get_error()


@pytest.mark.parametrize("response", [
    'No function tags here',  # No <function> tags
    '{"arg1": "value1"}',  # Just a plain JSON string
])
def test_parse_tool_response_missing_function(response):
    provider = ConcreteToolResponseParsingProvider(response)
    product = provider.parse_tool_response()
    assert not product.is_valid()
    assert product.get() is None
    assert "Expected a function call from the response" in product.get_error()
