from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from src.base.enums import TemplateType
from src.base.products.dict_product import DictProduct
from src.maps.commands.generate_place_command import GeneratePlaceCommand
from src.maps.factories.store_generated_place_command_factory import (
    StoreGeneratedPlaceCommandFactory,
)
from src.maps.templates_repository import TemplatesRepository
from src.prompting.providers.place_generation_tool_response_provider import (
    PlaceGenerationToolResponseProvider,
)


# Dummy classes for testing
class DummyPlace(BaseModel):
    name: str
    description: str


@pytest.fixture
def templates_repository_mock():
    return MagicMock(spec=TemplatesRepository)


@pytest.fixture
def place_generation_tool_response_provider_mock():
    return MagicMock(spec=PlaceGenerationToolResponseProvider)


@pytest.fixture
def store_generated_place_command_factory_mock():
    return MagicMock(spec=StoreGeneratedPlaceCommandFactory)


@pytest.fixture
def valid_place_data():
    return {
        "name": "Father Place",
        "categories": ["Category1", "Category2"],
        "description": "A description of the father place.",
    }


@pytest.fixture
def valid_product():
    product = MagicMock(spec=DictProduct)
    product.is_valid.return_value = True
    product.get.return_value = {
        "name": "Generated Place",
        "description": "Description of the generated place.",
        "type": "CustomType",
    }
    return product


def test_init_valid_arguments(
    templates_repository_mock,
    place_generation_tool_response_provider_mock,
    store_generated_place_command_factory_mock,
):
    command = GeneratePlaceCommand(
        place_template_type=TemplateType.AREA,
        father_place_template_type=TemplateType.REGION,
        father_place_name="ValidFatherPlace",
        place_generation_tool_response_provider=place_generation_tool_response_provider_mock,
        store_generated_place_command_factory=store_generated_place_command_factory_mock,
        templates_repository=templates_repository_mock,
    )
    assert command._father_place_name == "ValidFatherPlace"


def test_init_invalid_father_place_name(
    place_generation_tool_response_provider_mock,
    store_generated_place_command_factory_mock,
):
    with pytest.raises(ValueError) as exc_info:
        GeneratePlaceCommand(
            place_template_type=TemplateType.AREA,
            father_place_template_type=TemplateType.REGION,
            father_place_name="",
            place_generation_tool_response_provider=place_generation_tool_response_provider_mock,
            store_generated_place_command_factory=store_generated_place_command_factory_mock,
        )
    assert "'father_place_name' must be a non-empty string" in str(exc_info.value)


def test_validate_parent_template_type_valid():
    with patch.object(GeneratePlaceCommand, "__init__", lambda x: None):
        command = GeneratePlaceCommand()  # noqa
        command._place_template_type = TemplateType.AREA
        command._father_place_template_type = TemplateType.REGION
        command._validate_parent_template_type()


def test_validate_parent_template_type_invalid():
    with patch.object(GeneratePlaceCommand, "__init__", lambda x: None):
        command = GeneratePlaceCommand()  # noqa
        command._place_template_type = TemplateType.AREA
        command._father_place_template_type = TemplateType.WORLD
        with pytest.raises(ValueError) as exc_info:
            command._validate_parent_template_type()
        assert (
            "Attempted to create a 'area' from something other than a 'region'"
            in str(exc_info.value)
        )


def test_validate_parent_template_type_invalid_expected_parent():
    with patch.object(GeneratePlaceCommand, "__init__", lambda x: None):
        command = GeneratePlaceCommand()  # noqa
        command._place_template_type = TemplateType.STORY_UNIVERSE
        with pytest.raises(ValueError) as exc_info:
            command._validate_parent_template_type()
        assert "Invalid place_template_type: 'story_universe'" in str(exc_info.value)


def test_get_father_place_data_valid(templates_repository_mock, valid_place_data):
    templates_repository_mock.load_templates.return_value = {
        "FatherPlace": valid_place_data
    }
    with patch.object(GeneratePlaceCommand, "__init__", lambda x: None):
        command = GeneratePlaceCommand()  # noqa
        command._templates_repository = templates_repository_mock
        command._father_place_template_type = TemplateType.REGION
        command._father_place_name = "FatherPlace"
        father_place_data = command._get_father_place_data()
        assert father_place_data == valid_place_data


def test_get_father_place_data_invalid_name(templates_repository_mock):
    templates_repository_mock.load_templates.return_value = {}
    with patch.object(GeneratePlaceCommand, "__init__", lambda x: None):
        command = GeneratePlaceCommand()  # noqa
        command._templates_repository = templates_repository_mock
        command._father_place_template_type = TemplateType.REGION
        command._father_place_name = "NonExistentPlace"
        with pytest.raises(ValueError) as exc_info:
            command._get_father_place_data()
        assert (
            "There isn't a 'TemplateType.REGION' template named 'NonExistentPlace'."
            in str(exc_info.value)
        )


def test_get_categories_valid(valid_place_data):
    with patch.object(GeneratePlaceCommand, "__init__", lambda x: None):
        command = GeneratePlaceCommand()  # noqa
        categories = command._get_categories(valid_place_data)
        assert categories == ["category1", "category2"]


def test_get_categories_no_categories():
    father_place_data = {"name": "Father Place", "categories": []}
    with patch.object(GeneratePlaceCommand, "__init__", lambda x: None):
        command = GeneratePlaceCommand()  # noqa
        command._father_place_name = "Father Place"
        with pytest.raises(ValueError) as exc_info:
            command._get_categories(father_place_data)
        assert "There were no categories for father place 'Father Place'." in str(
            exc_info.value
        )


def test_get_place_class_valid():
    with patch.object(GeneratePlaceCommand, "__init__", lambda x: None):
        command = GeneratePlaceCommand()  # noqa
        command._place_template_type = TemplateType.LOCATION
        place_class = command._get_place_class()
        assert issubclass(place_class, BaseModel)


def test_get_place_class_not_implemented():
    with patch.object(GeneratePlaceCommand, "__init__", lambda x: None):
        command = GeneratePlaceCommand()  # noqa
        command._place_template_type = TemplateType.STORY_UNIVERSE
        with pytest.raises(NotImplementedError) as exc_info:
            command._get_place_class()
        assert (
            "Product generation not implemented for template type 'TemplateType.STORY_UNIVERSE'."
            in str(exc_info.value)
        )


def test_execute_successful(
    templates_repository_mock,
    place_generation_tool_response_provider_mock,
    store_generated_place_command_factory_mock,
    valid_place_data,
    valid_product,
):
    templates_repository_mock.load_templates.return_value = {
        "FatherPlace": valid_place_data
    }
    place_generation_tool_response_provider_mock.generate_product.return_value = (
        valid_product
    )
    store_command_mock = MagicMock()
    store_generated_place_command_factory_mock.create_command.return_value = (
        store_command_mock
    )

    command = GeneratePlaceCommand(
        place_template_type=TemplateType.AREA,
        father_place_template_type=TemplateType.REGION,
        father_place_name="FatherPlace",
        place_generation_tool_response_provider=place_generation_tool_response_provider_mock,
        store_generated_place_command_factory=store_generated_place_command_factory_mock,
        templates_repository=templates_repository_mock,
    )

    command.execute()

    store_command_mock.execute.assert_called_once()


def test_execute_invalid_tool_response(
    templates_repository_mock,
    place_generation_tool_response_provider_mock,
    store_generated_place_command_factory_mock,
    valid_place_data,
):
    templates_repository_mock.load_templates.return_value = {
        "FatherPlace": valid_place_data
    }
    invalid_product = MagicMock(spec=DictProduct)
    invalid_product.is_valid.return_value = False
    invalid_product.get_error.return_value = "Invalid response"
    place_generation_tool_response_provider_mock.generate_product.return_value = (
        invalid_product
    )

    command = GeneratePlaceCommand(
        place_template_type=TemplateType.AREA,
        father_place_template_type=TemplateType.REGION,
        father_place_name="FatherPlace",
        place_generation_tool_response_provider=place_generation_tool_response_provider_mock,
        store_generated_place_command_factory=store_generated_place_command_factory_mock,
        templates_repository=templates_repository_mock,
    )

    with pytest.raises(ValueError) as exc_info:
        command.execute()
    assert (
        "Unable to produce a tool response for 'area' generation: Invalid response"
        in str(exc_info.value)
    )


def test_execute_tool_response_error(
    templates_repository_mock,
    place_generation_tool_response_provider_mock,
    store_generated_place_command_factory_mock,
    valid_place_data,
):
    templates_repository_mock.load_templates.return_value = {
        "FatherPlace": valid_place_data
    }
    place_generation_tool_response_provider_mock.generate_product.side_effect = (
        Exception("Tool error")
    )

    command = GeneratePlaceCommand(
        place_template_type=TemplateType.AREA,
        father_place_template_type=TemplateType.REGION,
        father_place_name="FatherPlace",
        place_generation_tool_response_provider=place_generation_tool_response_provider_mock,
        store_generated_place_command_factory=store_generated_place_command_factory_mock,
        templates_repository=templates_repository_mock,
    )

    with pytest.raises(Exception) as exc_info:
        command.execute()
    assert "Tool error" in str(exc_info.value)


def test_execute_with_missing_father_place_data(
    templates_repository_mock,
    place_generation_tool_response_provider_mock,
    store_generated_place_command_factory_mock,
):
    templates_repository_mock.load_templates.return_value = {}
    command = GeneratePlaceCommand(
        place_template_type=TemplateType.AREA,
        father_place_template_type=TemplateType.REGION,
        father_place_name="NonExistentPlace",
        place_generation_tool_response_provider=place_generation_tool_response_provider_mock,
        store_generated_place_command_factory=store_generated_place_command_factory_mock,
        templates_repository=templates_repository_mock,
    )
    with pytest.raises(ValueError) as exc_info:
        command.execute()
    assert (
        "There isn't a 'TemplateType.REGION' template named 'NonExistentPlace'."
        in str(exc_info.value)
    )


def test_execute_with_missing_categories(
    templates_repository_mock,
    place_generation_tool_response_provider_mock,
    store_generated_place_command_factory_mock,
    valid_product,
):
    father_place_data = {"name": "FatherPlace", "categories": []}
    templates_repository_mock.load_templates.return_value = {
        "FatherPlace": father_place_data
    }
    place_generation_tool_response_provider_mock.generate_product.return_value = (
        valid_product
    )
    command = GeneratePlaceCommand(
        place_template_type=TemplateType.LOCATION,
        father_place_template_type=TemplateType.AREA,
        father_place_name="FatherPlace",
        place_generation_tool_response_provider=place_generation_tool_response_provider_mock,
        store_generated_place_command_factory=store_generated_place_command_factory_mock,
        templates_repository=templates_repository_mock,
    )
    with pytest.raises(ValueError) as exc_info:
        command.execute()
    assert "There were no categories for father place 'FatherPlace'." in str(
        exc_info.value
    )
