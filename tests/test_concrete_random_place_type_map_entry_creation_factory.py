from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from src.enums import PlaceType
from src.maps.abstracts.abstract_factories import (
    RandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.enums import RandomPlaceTypeMapEntryCreationResultType
from src.maps.factories.concrete_random_place_type_map_entry_creation_factory import (
    ConcreteRandomPlaceTypeMapEntryCreationFactory,
)


def test_init_with_empty_playthrough_name():
    with pytest.raises(ValueError) as excinfo:
        ConcreteRandomPlaceTypeMapEntryCreationFactory(
            playthrough_name="",
            father_template="father_template",
            place_type=PlaceType.AREA,
            father_place_type=PlaceType.REGION,
            random_place_template_based_on_categories_factory=cast(
                RandomPlaceTemplateBasedOnCategoriesFactory, MagicMock()
            ),
            create_map_entry_for_playthrough_command_factory=MagicMock(),
        )
    assert "'playthrough_name' can't be empty." in str(excinfo.value)


def test_init_with_empty_father_template():
    with pytest.raises(ValueError) as excinfo:
        ConcreteRandomPlaceTypeMapEntryCreationFactory(
            playthrough_name="playthrough_name",
            father_template="",
            place_type=PlaceType.AREA,
            father_place_type=PlaceType.REGION,
            random_place_template_based_on_categories_factory=cast(
                RandomPlaceTemplateBasedOnCategoriesFactory, MagicMock()
            ),
            create_map_entry_for_playthrough_command_factory=MagicMock(),
        )
    assert "'father_template' can't be empty." in str(excinfo.value)


@patch("src.maps.map_manager.MapManager")
@patch("src.filesystem.filesystem_manager.FilesystemManager")
def test_create_random_place_type_map_entry_no_available_templates(
        mock_filesystem_manager_class, mock_map_manager_class
):
    mock_filesystem_manager = mock_filesystem_manager_class.return_value
    mock_map_manager = mock_map_manager_class.return_value

    # Setup mock to return empty templates
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {}
    mock_map_manager.get_place_templates_of_type.return_value = []

    factory = ConcreteRandomPlaceTypeMapEntryCreationFactory(
        playthrough_name="playthrough_name",
        father_template="father_template",
        place_type=PlaceType.AREA,
        father_place_type=PlaceType.REGION,
        random_place_template_based_on_categories_factory=cast(
            RandomPlaceTemplateBasedOnCategoriesFactory, MagicMock()
        ),
        create_map_entry_for_playthrough_command_factory=MagicMock(),
        filesystem_manager=mock_filesystem_manager,
        map_manager=mock_map_manager,
    )

    result = factory.create_random_place_type_map_entry()

    assert (
            result.get_result_type()
            == RandomPlaceTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
    )


@patch("src.maps.map_manager.MapManager")
@patch("src.filesystem.filesystem_manager.FilesystemManager")
def test_create_random_place_type_map_entry_template_product_invalid(
        mock_filesystem_manager_class, mock_map_manager_class
):
    mock_filesystem_manager = mock_filesystem_manager_class.return_value
    mock_map_manager = mock_map_manager_class.return_value

    # Setup mock to return some templates
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {
        "template1": {}
    }
    mock_map_manager.get_place_templates_of_type.return_value = []

    # Mock PlaceTemplateProduct to return invalid
    mock_template_product = MagicMock()
    mock_template_product.is_valid.return_value = False
    mock_template_product.get_error.return_value = "Invalid template"

    mock_random_place_template_based_on_categories_factory = MagicMock()
    mock_random_place_template_based_on_categories_factory.create_random_place_template_based_on_categories.return_value = (
        mock_template_product
    )

    factory = ConcreteRandomPlaceTypeMapEntryCreationFactory(
        playthrough_name="playthrough_name",
        father_template="father_template",
        place_type=PlaceType.AREA,
        father_place_type=PlaceType.REGION,
        random_place_template_based_on_categories_factory=cast(
            RandomPlaceTemplateBasedOnCategoriesFactory,
            mock_random_place_template_based_on_categories_factory,
        ),
        create_map_entry_for_playthrough_command_factory=MagicMock(),
        filesystem_manager=mock_filesystem_manager,
        map_manager=mock_map_manager,
    )

    result = factory.create_random_place_type_map_entry()

    assert result.get_result_type() == RandomPlaceTypeMapEntryCreationResultType.FAILURE
    assert "Invalid template" in result.get_error()


@patch("src.maps.map_manager.MapManager")
@patch("src.filesystem.filesystem_manager.FilesystemManager")
def test_create_random_place_type_map_entry_success(
        mock_filesystem_manager_class, mock_map_manager_class
):
    mock_filesystem_manager = mock_filesystem_manager_class.return_value
    mock_map_manager = mock_map_manager_class.return_value

    # Setup mock to return some templates
    mock_filesystem_manager.load_existing_or_new_json_file.return_value = {
        "template1": {}
    }
    mock_map_manager.get_place_templates_of_type.return_value = []

    # Mock PlaceTemplateProduct to return valid
    mock_template_product = MagicMock()
    mock_template_product.is_valid.return_value = True
    mock_template_product.get.return_value = "template1"

    mock_random_place_template_based_on_categories_factory = MagicMock()
    mock_random_place_template_based_on_categories_factory.create_random_place_template_based_on_categories.return_value = (
        mock_template_product
    )

    mock_command = MagicMock()
    mock_create_map_entry_factory = MagicMock()
    mock_create_map_entry_factory.create_command.return_value = mock_command

    factory = ConcreteRandomPlaceTypeMapEntryCreationFactory(
        playthrough_name="playthrough_name",
        father_template="father_template",
        place_type=PlaceType.AREA,
        father_place_type=PlaceType.REGION,
        random_place_template_based_on_categories_factory=cast(
            RandomPlaceTemplateBasedOnCategoriesFactory,
            mock_random_place_template_based_on_categories_factory,
        ),
        create_map_entry_for_playthrough_command_factory=mock_create_map_entry_factory,
        filesystem_manager=mock_filesystem_manager,
        map_manager=mock_map_manager,
    )

    result = factory.create_random_place_type_map_entry()

    assert result.get_result_type() == RandomPlaceTypeMapEntryCreationResultType.SUCCESS
    mock_command.execute.assert_called_once()


@patch("src.maps.map_manager.MapManager")
@patch("src.filesystem.filesystem_manager.FilesystemManager")
def test_create_random_place_type_map_entry_exception(
        mock_filesystem_manager_class, mock_map_manager_class
):
    mock_filesystem_manager = mock_filesystem_manager_class.return_value
    mock_map_manager = mock_map_manager_class.return_value

    # Setup mock to raise exception
    mock_filesystem_manager.load_existing_or_new_json_file.side_effect = Exception(
        "File not found"
    )

    factory = ConcreteRandomPlaceTypeMapEntryCreationFactory(
        playthrough_name="playthrough_name",
        father_template="father_template",
        place_type=PlaceType.AREA,
        father_place_type=PlaceType.REGION,
        random_place_template_based_on_categories_factory=cast(
            RandomPlaceTemplateBasedOnCategoriesFactory, MagicMock()
        ),
        create_map_entry_for_playthrough_command_factory=MagicMock(),
        filesystem_manager=mock_filesystem_manager,
        map_manager=mock_map_manager,
    )

    result = factory.create_random_place_type_map_entry()

    assert result.get_result_type() == RandomPlaceTypeMapEntryCreationResultType.FAILURE
    assert "File not found" in result.get_error()
