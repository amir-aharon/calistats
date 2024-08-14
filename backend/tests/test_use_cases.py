from typing import TypeVar
import pytest
from unittest.mock import Mock
from datetime import datetime
from calistats.application.use_cases import create_stat, create_stat_type, get_stat_type
from calistats.domain.models import Stat, StatType
from calistats.domain.repositories import StatRepository, StatTypeRepository
from tests.utils import soft_compare

stat_data_1 = {"stat_type_id": 1, "owner_id": 1, "value": 100.0, "date": "2024-08-14T12:00:00"}
stat_data_2 = {"stat_type_id": 2, "owner_id": 2, "value": 50.0, "date": None}  # No date provided, should default
stat_type_data_1 = {"name": "Pushups", "unit": "reps"}
stat_type_data_2 = {"name": "Bench Press", "unit": "kg"}


@pytest.fixture
def stat_repo_mock():
    return Mock(StatRepository)


@pytest.fixture
def stat_type_repo_mock():
    return Mock(StatTypeRepository)


def test_create_stat(stat_repo_mock, stat_type_repo_mock):
    # Arrange
    stat_type_repo_mock.get = Mock(return_value=StatType(id=1, **stat_type_data_1))
    stat_repo_mock.add = Mock()

    expected_stat = Stat(id=1, **stat_data_1)

    # Act
    result_stat = create_stat(stat_repo_mock, stat_type_repo_mock, stat_data_1)

    # Assert
    stat_repo_mock.add.assert_called_once()
    added_stat = stat_repo_mock.add.call_args[0][0]
    assert soft_compare(added_stat, expected_stat)
    assert soft_compare(result_stat, expected_stat)


def test_create_stat_with_default_date(stat_repo_mock, stat_type_repo_mock):
    # Arrange
    stat_type_repo_mock.get = Mock(return_value=StatType(id=2, **stat_type_data_2))
    stat_repo_mock.add = Mock()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    expected_stat = Stat(id=1, **{**stat_data_2, "date": now})

    # Act
    result_stat = create_stat(stat_repo_mock, stat_type_repo_mock, stat_data_2)

    # Assert
    stat_repo_mock.add.assert_called_once()
    added_stat = stat_repo_mock.add.call_args[0][0]
    assert soft_compare(added_stat, expected_stat)
    assert soft_compare(result_stat, expected_stat)


def test_create_stat_type(stat_type_repo_mock):
    # Arrange
    stat_type_repo_mock.add = Mock()
    expected_stat_type = StatType(id=1, **stat_type_data_1)

    # Act
    result_stat_type = create_stat_type(stat_type_repo_mock, stat_type_data_1)

    # Assert
    stat_type_repo_mock.add.assert_called_once()
    added_stat_type = stat_type_repo_mock.add.call_args[0][0]
    assert soft_compare(added_stat_type, expected_stat_type)
    assert soft_compare(result_stat_type, expected_stat_type)


def test_get_stat_type(stat_type_repo_mock):
    # Arrange
    stat_type_id = 1
    expected_stat_type = StatType(id=stat_type_id, **stat_type_data_1)
    stat_type_repo_mock.get = Mock(return_value=expected_stat_type)

    # Act
    result_stat_type = get_stat_type(stat_type_repo_mock, stat_type_id)

    # Assert
    stat_type_repo_mock.get.assert_called_once_with(stat_type_id)
    assert result_stat_type == expected_stat_type


def test_get_stat_type_not_found(stat_type_repo_mock):
    # Arrange
    stat_type_id = 999
    stat_type_repo_mock.get = Mock(return_value=None)

    # Act
    result_stat_type = get_stat_type(stat_type_repo_mock, stat_type_id)

    # Assert
    stat_type_repo_mock.get.assert_called_once_with(stat_type_id)
    assert result_stat_type is None


@pytest.mark.parametrize(
    "stat_data, expected_stat",
    [
        (
            {"stat_type_id": 1, "owner_id": 1, "value": 100.0, "date": "2024-08-14T12:00:00"},
            Stat(id=1, stat_type_id=1, owner_id=1, value=100.0, date="2024-08-14T12:00:00"),
        ),
        (
            {"stat_type_id": 2, "owner_id": 2, "value": 50.0, "date": None},
            Stat(id=1, stat_type_id=2, owner_id=2, value=50.0, date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
        ),
    ],
)
def test_create_stat_parametrized(stat_repo_mock, stat_type_repo_mock, stat_data, expected_stat):
    # Arrange
    stat_repo_mock.add = Mock()
    stat_type_repo_mock.get = Mock(return_value=StatType(id=1, name="Test", unit="reps"))

    # Act
    result_stat = create_stat(stat_repo_mock, stat_type_repo_mock, stat_data)

    # Assert
    stat_repo_mock.add.assert_called_once()
    assert soft_compare(result_stat, expected_stat)


@pytest.mark.parametrize(
    "stat_type_data, expected_stat_type",
    [
        ({"name": "Pushups", "unit": "reps"}, StatType(id=1, name="Pushups", unit="reps")),
        ({"name": "Bench Press", "unit": "kg"}, StatType(id=2, name="Bench Press", unit="kg")),
        ({"name": "Squats", "unit": "reps"}, StatType(id=3, name="Squats", unit="reps")),
    ],
)
def test_create_stat_type_parametrized(stat_type_repo_mock, stat_type_data, expected_stat_type):
    # Arrange
    stat_type_repo_mock.add = Mock()

    # Act
    result_stat_type = create_stat_type(stat_type_repo_mock, stat_type_data)

    # Assert
    stat_type_repo_mock.add.assert_called_once()
    assert soft_compare(result_stat_type, expected_stat_type)
