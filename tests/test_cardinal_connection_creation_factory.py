# test_cardinal_connection_creation_factory.py

from unittest.mock import Mock

from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.required_string import RequiredString
from src.maps.configs.cardinal_connection_creation_factory_config import (
    CardinalConnectionCreationFactoryConfig,
)
from src.maps.configs.cardinal_connection_creation_factory_factories_config import (
    CardinalConnectionCreationFactoryFactoriesConfig,
)
from src.maps.enums import (
    CardinalDirection,
    RandomTemplateTypeMapEntryCreationResultType,
)
from src.maps.factories.concrete_cardinal_connection_creation_factory import (
    ConcreteCardinalConnectionCreationFactory,
)
from src.maps.products.concrete_cardinal_connection_creation_product import (
    ConcreteCardinalConnectionCreationProduct,
)


def test_create_cardinal_connection_no_available_templates():
    # Mock the PlaythroughManager
    playthrough_manager_mock = Mock(spec=PlaythroughManager)
    playthrough_manager_mock.get_current_place_identifier.return_value = "current_place"

    # Mock RandomTemplateTypeMapEntryCreationResult with NO_AVAILABLE_TEMPLATES
    random_area_result_mock = Mock()
    random_area_result_mock.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.NO_AVAILABLE_TEMPLATES
    )

    # Mock dependencies
    map_manager_factory_mock = Mock()
    hierarchy_manager_factory_mock = Mock()
    navigation_manager_factory_mock = Mock()
    random_template_provider_factory_mock = Mock()

    # Set up the factories config
    factories_config = CardinalConnectionCreationFactoryFactoriesConfig(
        random_template_type_map_entry_provider_factory=random_template_provider_factory_mock,
        hierarchy_manager_factory=hierarchy_manager_factory_mock,
        map_manager_factory=map_manager_factory_mock,
        navigation_manager_factory=navigation_manager_factory_mock,
    )

    # Set up the main config
    config = CardinalConnectionCreationFactoryConfig(
        playthrough_name=RequiredString("test_playthrough"),
        cardinal_direction=CardinalDirection.NORTH,
    )

    # Instantiate the factory
    factory = ConcreteCardinalConnectionCreationFactory(
        config=config,
        factories_config=factories_config,
        playthrough_manager=playthrough_manager_mock,
    )

    # Mock the _get_random_area method
    factory._get_random_area = Mock(return_value=random_area_result_mock)

    # Invoke the method under test
    product = factory.create_cardinal_connection()

    # Assert the expected outcome
    assert isinstance(product, ConcreteCardinalConnectionCreationProduct)
    assert not product.was_successful()
    assert product.get_error() == "No remaining areas to add to map."


def test_create_cardinal_connection_failure():
    # Mock the PlaythroughManager
    playthrough_manager_mock = Mock(spec=PlaythroughManager)
    playthrough_manager_mock.get_current_place_identifier.return_value = "current_place"

    # Mock RandomTemplateTypeMapEntryCreationResult with FAILURE
    random_area_result_mock = Mock()
    random_area_result_mock.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.FAILURE
    )
    random_area_result_mock.get_error.return_value = "Some error occurred"

    # Mock dependencies
    map_manager_factory_mock = Mock()
    hierarchy_manager_factory_mock = Mock()
    navigation_manager_factory_mock = Mock()
    random_template_provider_factory_mock = Mock()

    # Set up the factories config
    factories_config = CardinalConnectionCreationFactoryFactoriesConfig(
        random_template_type_map_entry_provider_factory=random_template_provider_factory_mock,
        hierarchy_manager_factory=hierarchy_manager_factory_mock,
        map_manager_factory=map_manager_factory_mock,
        navigation_manager_factory=navigation_manager_factory_mock,
    )

    # Set up the main config
    config = CardinalConnectionCreationFactoryConfig(
        playthrough_name=RequiredString("test_playthrough"),
        cardinal_direction=CardinalDirection.EAST,
    )

    # Instantiate the factory
    factory = ConcreteCardinalConnectionCreationFactory(
        config=config,
        factories_config=factories_config,
        playthrough_manager=playthrough_manager_mock,
    )

    # Mock the _get_random_area method
    factory._get_random_area = Mock(return_value=random_area_result_mock)

    # Invoke the method under test
    product = factory.create_cardinal_connection()

    # Assert the expected outcome
    assert isinstance(product, ConcreteCardinalConnectionCreationProduct)
    assert not product.was_successful()
    expected_error = "Couldn't add an area east: Some error occurred"
    assert product.get_error() == expected_error


def test_create_cardinal_connection_success():
    # Mock the PlaythroughManager
    playthrough_manager_mock = Mock(spec=PlaythroughManager)
    playthrough_manager_mock.get_current_place_identifier.return_value = "current_place"

    # Mock RandomTemplateTypeMapEntryCreationResult with SUCCESS
    random_area_result_mock = Mock()
    random_area_result_mock.get_result_type.return_value = (
        RandomTemplateTypeMapEntryCreationResultType.SUCCESS
    )

    # Mock MapManager and its methods
    map_manager_mock = Mock()
    map_manager_mock.get_father_template.return_value = TemplateType.REGION
    map_manager_mock.get_identifier_and_place_template_of_latest_map_entry.return_value = (
        "new_place_id",
        TemplateType.AREA,
    )

    map_manager_factory_mock = Mock()
    map_manager_factory_mock.create_map_manager.return_value = map_manager_mock

    # Mock HierarchyManager and its methods
    hierarchy_manager_mock = Mock()
    hierarchy_manager_mock.get_father_identifier.return_value = "father_identifier"

    hierarchy_manager_factory_mock = Mock()
    hierarchy_manager_factory_mock.create_hierarchy_manager.return_value = (
        hierarchy_manager_mock
    )

    # Mock NavigationManager and its methods
    navigation_manager_mock = Mock()
    navigation_manager_mock.get_opposite_cardinal_direction.return_value = (
        CardinalDirection.SOUTH
    )
    navigation_manager_mock.create_cardinal_connection = Mock()

    navigation_manager_factory_mock = Mock()
    navigation_manager_factory_mock.create_navigation_manager.return_value = (
        navigation_manager_mock
    )

    # Mock RandomTemplateTypeMapEntryProvider and its methods
    random_template_provider_mock = Mock()
    random_template_provider_mock.create_random_place_type_map_entry.return_value = (
        random_area_result_mock
    )

    random_template_provider_factory_mock = Mock()
    random_template_provider_factory_mock.create_provider.return_value = (
        random_template_provider_mock
    )

    # Set up the factories config
    factories_config = CardinalConnectionCreationFactoryFactoriesConfig(
        random_template_type_map_entry_provider_factory=random_template_provider_factory_mock,
        hierarchy_manager_factory=hierarchy_manager_factory_mock,
        map_manager_factory=map_manager_factory_mock,
        navigation_manager_factory=navigation_manager_factory_mock,
    )

    # Set up the main config
    config = CardinalConnectionCreationFactoryConfig(
        playthrough_name=RequiredString("test_playthrough"),
        cardinal_direction=CardinalDirection.NORTH,
    )

    # Instantiate the factory
    factory = ConcreteCardinalConnectionCreationFactory(
        config=config,
        factories_config=factories_config,
        playthrough_manager=playthrough_manager_mock,
    )

    # Invoke the method under test
    product = factory.create_cardinal_connection()

    # Assert the expected outcome
    assert isinstance(product, ConcreteCardinalConnectionCreationProduct)
    assert product.was_successful()
    assert product.get_error() is None

    # Assert that the NavigationManager's create_cardinal_connection was called twice
    assert navigation_manager_mock.create_cardinal_connection.call_count == 2

    # Assert that the correct parameters were passed in the first call
    navigation_manager_mock.create_cardinal_connection.assert_any_call(
        CardinalDirection.NORTH,
        RequiredString("current_place"),
        "new_place_id",
    )

    # Assert that the correct parameters were passed in the second call
    navigation_manager_mock.create_cardinal_connection.assert_any_call(
        CardinalDirection.SOUTH,
        "new_place_id",
        RequiredString("current_place"),
    )
