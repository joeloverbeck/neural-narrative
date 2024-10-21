import pytest

from src.base.required_string import RequiredString


def test_required_string_raises_value_error_on_empty_string():
    with pytest.raises(ValueError) as exc_info:
        RequiredString("")
    assert "value can't be empty." in str(exc_info.value)


def test_required_string_raises_type_error_on_non_string():
    with pytest.raises(TypeError) as exc_info:
        RequiredString(123)
    assert "value must be a string" in str(exc_info.value)


def test_required_string_initializes_with_required_string():
    rs1 = RequiredString("test")
    rs2 = RequiredString(rs1)
    assert rs2.value == "test"


def test_required_string_equality():
    rs1 = RequiredString("test")
    rs2 = RequiredString("test")
    rs3 = RequiredString("different")
    assert rs1 == rs2
    assert rs1 != rs3


def test_required_string_less_than():
    rs1 = RequiredString("abc")
    rs2 = RequiredString("def")
    assert rs1 < rs2
    assert not rs2 < rs1


def test_required_string_str():
    rs = RequiredString("test")
    assert str(rs) == "test"


# Additional Test: Verify that RequiredString raises ValueError for empty string
def test_required_string_empty_string():
    with pytest.raises(ValueError) as exc_info:
        RequiredString("")
    assert str(exc_info.value) == "value can't be empty."


# Additional Test: Verify that RequiredString correctly initializes with valid string
def test_required_string_valid():
    rs = RequiredString("Valid String")
    assert rs.value == "Valid String"
    assert str(rs) == "Valid String"


# Additional Test: Test ordering and equality of RequiredString
def test_required_string_ordering_and_equality():
    rs1 = RequiredString("Alpha")
    rs2 = RequiredString("Beta")
    rs3 = RequiredString("Alpha")

    assert rs1 < rs2
    assert rs2 > rs1
    assert rs1 == rs3
    assert rs1 != rs2
