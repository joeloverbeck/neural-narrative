from typing import cast
from unittest.mock import Mock

import pytest

from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.filesystem.filesystem_manager import FilesystemManager


class MockProduct:

    @staticmethod
    def is_valid():
        return True

    @staticmethod
    def get():
        return ["item1", "item2"]

    @staticmethod
    def get_error():
        return "Mock error message"


class MockConceptFactory:

    @staticmethod
    def generate_product():
        return MockProduct()


class MockFilesystemManager:

    def __init__(self):
        self.saved_content = ""

    def append_to_file(self, file_path, content):
        self.saved_content += str(content)


class TestConceptAlgorithm(BaseConceptAlgorithm):

    def get_save_file_path(self) -> str:
        return "test_save_file.txt"


def test_init_valid():
    playthrough_name = "TestPlaythrough"
    concept_factory = MockConceptFactory()
    filesystem_manager = MockFilesystemManager()
    algorithm = TestConceptAlgorithm(
        playthrough_name, concept_factory, cast(FilesystemManager, filesystem_manager)
    )
    assert algorithm._playthrough_name == playthrough_name
    assert algorithm._concept_factory == concept_factory
    assert algorithm._filesystem_manager == filesystem_manager


def test_do_algorithm_normal():
    playthrough_name = "TestPlaythrough"
    concept_factory = MockConceptFactory()
    filesystem_manager = MockFilesystemManager()
    algorithm = TestConceptAlgorithm(
        playthrough_name, concept_factory, cast(FilesystemManager, filesystem_manager)
    )
    generated_items = algorithm.do_algorithm()
    assert generated_items == ["item1", "item2"]
    assert filesystem_manager.saved_content == "item1\nitem2"


def test_do_algorithm_invalid_product():
    playthrough_name = "TestPlaythrough"

    class InvalidMockProduct:

        @staticmethod
        def is_valid():
            return False

        @staticmethod
        def get_error():
            return "Invalid product"

    class InvalidMockConceptFactory:

        @staticmethod
        def generate_product():
            return InvalidMockProduct()

    concept_factory = InvalidMockConceptFactory()
    filesystem_manager = MockFilesystemManager()
    algorithm = TestConceptAlgorithm(
        playthrough_name, concept_factory, cast(FilesystemManager, filesystem_manager)
    )
    with pytest.raises(ValueError) as exc_info:
        algorithm.do_algorithm()
    assert "Failed to generate product" in str(exc_info)


def test_do_algorithm_empty_generated_items():
    playthrough_name = "TestPlaythrough"

    class EmptyMockProduct:

        @staticmethod
        def is_valid():
            return True

        @staticmethod
        def get():
            return []

    class EmptyMockConceptFactory:

        @staticmethod
        def generate_product():
            return EmptyMockProduct()

    concept_factory = EmptyMockConceptFactory()
    filesystem_manager = MockFilesystemManager()
    algorithm = TestConceptAlgorithm(
        playthrough_name, concept_factory, cast(FilesystemManager, filesystem_manager)
    )
    with pytest.raises(ValueError) as exc_info:
        algorithm.do_algorithm()
    assert "No items were generated" in str(exc_info)


def test_save_generated_items_calls_filesystem_manager():
    playthrough_name = "TestPlaythrough"
    concept_factory = MockConceptFactory()
    filesystem_manager = Mock()
    algorithm = TestConceptAlgorithm(
        playthrough_name, concept_factory, filesystem_manager
    )
    items = ["item1", "item2"]
    algorithm.save_generated_items(items)
    filesystem_manager.append_to_file.assert_called_once()
    args, kwargs = filesystem_manager.append_to_file.call_args
    file_path_arg = args[0]
    content_arg = args[1]
    assert file_path_arg == "test_save_file.txt"
    assert content_arg == "item1\nitem2"


def test_save_generated_items_empty():
    playthrough_name = "TestPlaythrough"
    concept_factory = MockConceptFactory()
    filesystem_manager = MockFilesystemManager()
    algorithm = TestConceptAlgorithm(
        playthrough_name, concept_factory, cast(FilesystemManager, filesystem_manager)
    )
    items = []
    with pytest.raises(ValueError) as exc_info:
        algorithm.save_generated_items(items)
    assert "There weren't items to save." in str(exc_info)


def test_get_save_file_path_not_implemented():
    playthrough_name = "TestPlaythrough"
    concept_factory = MockConceptFactory()
    filesystem_manager = MockFilesystemManager()

    class IncompleteAlgorithm(BaseConceptAlgorithm):
        pass

    algorithm = IncompleteAlgorithm(
        playthrough_name, concept_factory, cast(FilesystemManager, filesystem_manager)
    )
    with pytest.raises(NotImplementedError):
        algorithm.get_save_file_path()
