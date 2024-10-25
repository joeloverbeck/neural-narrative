from unittest.mock import MagicMock, patch

import pytest

from src.base.enums import TemplateType
from src.maps.algorithms.filter_out_used_templates_algorithm import (
    FilterOutUsedTemplatesAlgorithm,
)


class TestFilterOutUsedTemplatesAlgorithm:

    def test_filter_out_used_templates_basic(self):
        """Test basic functionality where some templates are used and some are not."""
        # Arrange
        place_type = TemplateType.LOCATION

        # Mock PlaceManager and its method
        mock_place_manager = MagicMock()
        mock_place_manager.get_places_of_type.return_value = ["template1", "template3"]

        # Mock PlaceManagerFactory and its method
        mock_place_manager_factory = MagicMock()
        mock_place_manager_factory.create_place_manager.return_value = (
            mock_place_manager
        )

        # Mock TemplatesRepository and its method
        available_templates = {
            "template1": {"data": "data1"},
            "template2": {"data": "data2"},
            "template3": {"data": "data3"},
        }
        mock_templates_repository = MagicMock()
        mock_templates_repository.load_template.return_value = available_templates

        # Instantiate the class with mocks
        algorithm = FilterOutUsedTemplatesAlgorithm(
            place_type=place_type,
            place_manager_factory=mock_place_manager_factory,
            templates_repository=mock_templates_repository,
        )

        # Act
        result = algorithm.do_algorithm()

        # Assert
        expected_output = {"template2": {"data": "data2"}}
        assert result == expected_output

    def test_filter_out_used_templates_no_used_templates(self):
        """Test when no templates are used."""
        # Arrange
        place_type = TemplateType.AREA

        # Mock PlaceManager and its method
        mock_place_manager = MagicMock()
        mock_place_manager.get_places_of_type.return_value = []

        # Mock PlaceManagerFactory and its method
        mock_place_manager_factory = MagicMock()
        mock_place_manager_factory.create_place_manager.return_value = (
            mock_place_manager
        )

        # Mock TemplatesRepository and its method
        available_templates = {
            "template1": {"data": "data1"},
            "template2": {"data": "data2"},
        }
        mock_templates_repository = MagicMock()
        mock_templates_repository.load_template.return_value = available_templates

        # Instantiate the class with mocks
        algorithm = FilterOutUsedTemplatesAlgorithm(
            place_type=place_type,
            place_manager_factory=mock_place_manager_factory,
            templates_repository=mock_templates_repository,
        )

        # Act
        result = algorithm.do_algorithm()

        # Assert
        expected_output = {
            "template1": {"data": "data1"},
            "template2": {"data": "data2"},
        }
        assert result == expected_output

    def test_filter_out_used_templates_all_used_templates(self):
        """Test when all templates are used."""
        # Arrange
        place_type = TemplateType.REGION

        # Mock PlaceManager and its method
        mock_place_manager = MagicMock()
        mock_place_manager.get_places_of_type.return_value = ["template1", "template2"]

        # Mock PlaceManagerFactory and its method
        mock_place_manager_factory = MagicMock()
        mock_place_manager_factory.create_place_manager.return_value = (
            mock_place_manager
        )

        # Mock TemplatesRepository and its method
        available_templates = {
            "template1": {"data": "data1"},
            "template2": {"data": "data2"},
        }
        mock_templates_repository = MagicMock()
        mock_templates_repository.load_template.return_value = available_templates

        # Instantiate the class with mocks
        algorithm = FilterOutUsedTemplatesAlgorithm(
            place_type=place_type,
            place_manager_factory=mock_place_manager_factory,
            templates_repository=mock_templates_repository,
        )

        # Act
        result = algorithm.do_algorithm()

        # Assert
        expected_output = {}
        assert result == expected_output

    def test_filter_out_used_templates_no_available_templates(self):
        """Test when there are no available templates."""
        # Arrange
        place_type = TemplateType.WORLD

        # Mock PlaceManager and its method
        mock_place_manager = MagicMock()
        mock_place_manager.get_places_of_type.return_value = []

        # Mock PlaceManagerFactory and its method
        mock_place_manager_factory = MagicMock()
        mock_place_manager_factory.create_place_manager.return_value = (
            mock_place_manager
        )

        # Mock TemplatesRepository and its method
        available_templates = {}
        mock_templates_repository = MagicMock()
        mock_templates_repository.load_template.return_value = available_templates

        # Instantiate the class with mocks
        algorithm = FilterOutUsedTemplatesAlgorithm(
            place_type=place_type,
            place_manager_factory=mock_place_manager_factory,
            templates_repository=mock_templates_repository,
        )

        # Act
        result = algorithm.do_algorithm()

        # Assert
        expected_output = {}
        assert result == expected_output

    def test_filter_out_used_templates_exception_loading_templates(self):
        """Test exception handling when loading templates fails."""
        # Arrange
        place_type = TemplateType.STORY_UNIVERSE

        # Mock PlaceManager and its method
        mock_place_manager = MagicMock()
        mock_place_manager.get_places_of_type.return_value = []

        # Mock PlaceManagerFactory and its method
        mock_place_manager_factory = MagicMock()
        mock_place_manager_factory.create_place_manager.return_value = (
            mock_place_manager
        )

        # Mock TemplatesRepository to raise an exception
        mock_templates_repository = MagicMock()
        mock_templates_repository.load_template.side_effect = ValueError(
            "Template file not found."
        )

        # Instantiate the class with mocks
        algorithm = FilterOutUsedTemplatesAlgorithm(
            place_type=place_type,
            place_manager_factory=mock_place_manager_factory,
            templates_repository=mock_templates_repository,
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            algorithm.do_algorithm()

        assert "Template file not found." in str(exc_info.value)

    def test_filter_out_used_templates_default_templates_repository(self):
        """Test using the default TemplatesRepository when none is provided."""
        # Arrange
        place_type = TemplateType.LOCATION

        # Mock PlaceManager and its method
        mock_place_manager = MagicMock()
        mock_place_manager.get_places_of_type.return_value = []

        # Mock PlaceManagerFactory and its method
        mock_place_manager_factory = MagicMock()
        mock_place_manager_factory.create_place_manager.return_value = (
            mock_place_manager
        )

        # Patch TemplatesRepository to avoid real file system interactions
        with patch(
            "src.maps.algorithms.filter_out_used_templates_algorithm.TemplatesRepository"
        ) as MockTemplatesRepository:
            mock_templates_repository = MockTemplatesRepository.return_value
            available_templates = {
                "template1": {"data": "data1"},
                "template2": {"data": "data2"},
            }
            mock_templates_repository.load_template.return_value = available_templates

            # Instantiate the class without providing templates_repository
            algorithm = FilterOutUsedTemplatesAlgorithm(
                place_type=place_type,
                place_manager_factory=mock_place_manager_factory,
            )

            # Act
            result = algorithm.do_algorithm()

            # Assert
            expected_output = {
                "template1": {"data": "data1"},
                "template2": {"data": "data2"},
            }
            assert result == expected_output

    def test_filter_out_used_templates_different_place_types(self):
        """Test the algorithm with different TemplateType enums."""
        for place_type in TemplateType:
            # Arrange
            # Mock PlaceManager and its method
            mock_place_manager = MagicMock()
            mock_place_manager.get_places_of_type.return_value = ["template1"]

            # Mock PlaceManagerFactory and its method
            mock_place_manager_factory = MagicMock()
            mock_place_manager_factory.create_place_manager.return_value = (
                mock_place_manager
            )

            # Mock TemplatesRepository and its method
            available_templates = {
                "template1": {"data": "data1"},
                "template2": {"data": "data2"},
            }
            mock_templates_repository = MagicMock()
            mock_templates_repository.load_template.return_value = available_templates

            # Instantiate the class with mocks
            algorithm = FilterOutUsedTemplatesAlgorithm(
                place_type=place_type,
                place_manager_factory=mock_place_manager_factory,
                templates_repository=mock_templates_repository,
            )

            # Act
            result = algorithm.do_algorithm()

            # Assert
            expected_output = {
                "template2": {"data": "data2"},
            }
            assert result == expected_output
