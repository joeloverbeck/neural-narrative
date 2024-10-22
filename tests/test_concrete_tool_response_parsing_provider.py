import pytest
from src.prompting.providers.concrete_tool_response_parsing_provider import (
    ConcreteToolResponseParsingProvider,
)


@pytest.mark.parametrize(
    "input_json, expected_output",
    [
        (
            {" key1 ": "value1", " key2 ": {" nested key ": "value2"}},
            {"key1": "value1", "key2": {"nested key": "value2"}},
        ),
        ({" key ": [{" nested_key ": "value"}]}, {"key": [{"nested_key": "value"}]}),
    ],
)
def test_clean_json_keys(input_json, expected_output):
    provider = ConcreteToolResponseParsingProvider("dummy")
    assert provider._clean_json_keys(input_json) == expected_output


@pytest.mark.parametrize(
    "response, expected_function_name, expected_arguments",
    [
        (
            '<function=myFunction>{"arg1": "value1", "arg2": 2}</function>',
            "myFunction",
            {"arg1": "value1", "arg2": 2},
        ),
        (
            '<function=otherFunction>{"arg": true}</function>',
            "otherFunction",
            {"arg": True},
        ),
    ],
)
def test_parse_tool_response_success(
    response, expected_function_name, expected_arguments
):
    provider = ConcreteToolResponseParsingProvider(response)
    product = provider.parse_tool_response()
    assert product.is_valid()
    assert product.get()["function"] == expected_function_name
    assert product.get()["arguments"] == expected_arguments
    assert product.get_error() is None


@pytest.mark.parametrize(
    "response",
    [
        '<function=myFunction>{"arg1": "value1", "arg2": } </function>',
        '<function=myFunction>{"arg1": "value1"</function>',
    ],
)
def test_parse_tool_response_json_error(response):
    provider = ConcreteToolResponseParsingProvider(response)
    product = provider.parse_tool_response()
    assert not product.is_valid()
    assert product.get() is None
    assert "Error parsing function arguments" in product.get_error()


@pytest.mark.parametrize("response", ["No function tags here", '{"arg1": "value1"}'])
def test_parse_tool_response_missing_function(response):
    provider = ConcreteToolResponseParsingProvider(response)
    product = provider.parse_tool_response()
    assert not product.is_valid()
    assert product.get() is None
    assert "Expected a function call from the response" in product.get_error()


def test_valid_tool_response():
    response = '<function=generate_region>{"name": "Zoopolis", "description": "A diverse world teeming with sentient species.", "categories": ["Fantasy World", "Sentient Species"]}</function>'
    provider = ConcreteToolResponseParsingProvider(response)
    result = provider.parse_tool_response()
    assert result.is_valid() is True
    assert result.get()["function"] == "generate_region"
    assert result.get()["arguments"]["name"] == "Zoopolis"
    assert result.get()["arguments"]["categories"] == [
        "Fantasy World",
        "Sentient Species",
    ]


def test_single_quotes_in_content_gets_parsed_properly():
    response = '<function=generate_region>{"name": "Zoopolis", "description": "A diverse world teeming with sentient species.", "categories": [\'Fantasy World\', \'Sentient Species\']}</function>'
    provider = ConcreteToolResponseParsingProvider(response)
    result = provider.parse_tool_response()
    assert result.is_valid() is True


def test_missing_function_tag():
    response = '{"name": "Zoopolis", "description": "A diverse world teeming with sentient species."}'
    provider = ConcreteToolResponseParsingProvider(response)
    result = provider.parse_tool_response()
    assert result.is_valid() is False
    assert "Expected a function call from the response" in result.get_error()


def test_parse_tool_response_valid():
    response = "<function=generate_area>{\"name\": \"Savannah's Cradle\", \"description\": \"Savannah's Cradle is a vast expanse of rolling grasslands and savannas, bordered by the steep cliffs of the region's eastern mountain range. This area is characterized by its open skies and endless horizons, broken only by the occasional acacia tree or rocky outcropping. The soil in Savannah's Cradle is rich and fertile, supporting a diverse array of plant life, including the rare Savasagra herb, prized for its medicinal properties. The area is also home to vast herds of grazing animals, such as zebra and antelope, which in turn support a healthy population of predators, including the iconic Nexorian lion. Savannah's Cradle is crisscrossed by a network of well-worn trails, which serve as trade routes for the region's many caravans and travelers. The area is dominated by the Lion Folk, who maintain a strong presence in the area and serve as its primary defenders. They are governed by a council of elders, who meet regularly in the Great Boma, a massive circular meeting hall located in the heart of the savanna. The people of Savannah's Cradle are deeply spiritual, with a strong belief in the power of the ancestors. The area is dotted with sacred sites, including the Tower of Winds, a soaring spire adorned with intricate carvings that whistles hauntingly in the breeze. The tower is said to be a conduit for the spirits of the departed, who watch over the living from the great beyond. Despite its many wonders, Savannah's Cradle is not without its dangers. The mountain passes to the east are treacherous and prone to rockslides, while the grasslands themselves are home to hidden sinkholes and treacherous bogs. There are also whispers of an ancient evil that slumbers beneath the savanna, waiting to be awakened by the foolish or the unwary.\"}</function>"
    parsing_provider = ConcreteToolResponseParsingProvider(response)
    parsed_response = parsing_provider.parse_tool_response()
    assert parsed_response.is_valid() is True
    assert parsed_response.get() is not None
    assert parsed_response.get()["function"] == "generate_area"
    assert parsed_response.get()["arguments"]["name"] == "Savannah's Cradle"


def test_parse_tool_response_invalid_json():
    response = '<function=generate_area>{"name": "Savannah\'s Cradle", "description": "This is an invalid JSON object because of a missing quote}</function>'
    parsing_provider = ConcreteToolResponseParsingProvider(response)
    parsed_response = parsing_provider.parse_tool_response()
    assert parsed_response.is_valid() is False
    assert "Error parsing function arguments" in parsed_response.get_error()


def test_parse_tool_response_no_function_call():
    response = "This is a random string without a function call"
    parsing_provider = ConcreteToolResponseParsingProvider(response)
    parsed_response = parsing_provider.parse_tool_response()
    assert parsed_response.is_valid() is False
    assert "Expected a function call" in parsed_response.get_error()
