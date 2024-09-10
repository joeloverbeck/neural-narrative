import pytest

from src.time.time_manager import TimeManager


def test_initial_time_valid():
    tm = TimeManager(5)
    assert tm.get_hour() == 5


def test_get_time_of_day_morning():
    tm = TimeManager(8)
    assert tm.get_time_of_the_day() == "in the morning"


def test_get_time_of_day_afternoon():
    tm = TimeManager(13)
    assert tm.get_time_of_the_day() == "in the afternoon"


def test_get_time_of_day_evening():
    tm = TimeManager(19)
    assert tm.get_time_of_the_day() == "in the evening"


def test_get_time_of_day_night():
    tm = TimeManager(23)
    assert tm.get_time_of_the_day() == "at night"


def test_advance_time():
    tm = TimeManager(22)
    tm.advance_time(5)
    assert tm.get_hour() == 3
    assert tm.get_time_of_the_day() == "at night"


def test_advance_time_no_wrap():
    tm = TimeManager(10)
    tm.advance_time(2)
    assert tm.get_hour() == 12
    assert tm.get_time_of_the_day() == "in the afternoon"


def test_invalid_initial_time():
    with pytest.raises(ValueError):
        TimeManager(25)
