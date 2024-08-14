import pytest
from unittest.mock import Mock
from calistats.domain.models import Stat
from calistats.application.stat_use_cases import create_stat, get_stat_by_id, delete_stat_by_id


@pytest.fixture
def stat_repo_mock():
    return Mock()


@pytest.fixture
def stat_type_repo_mock():
    return Mock()


@pytest.fixture
def stat_data():
    return {"user_id": 1, "stat_type_id": 1, "value": 100.0, "date": None}  # Allow it to be auto-generated in the test


@pytest.fixture
def stat():
    return Stat(id=1, user_id=1, stat_type_id=1, value=100.0, date="2024-08-14T00:00:00")


def assert_stat_equal(stat1: Stat, stat2: Stat):
    """Utility function to compare two Stat objects, ignoring 'id' field."""
    assert stat1.user_id == stat2.user_id
    assert stat1.stat_type_id == stat2.stat_type_id
    assert stat1.value == stat2.value
    assert stat1.date == stat2.date


def test_create_stat(stat_repo_mock, stat_type_repo_mock, stat_data):
    # Arrange
    stat_repo_mock.add = Mock()
    stat_type_repo_mock.get.return_value = Mock(id=1)

    # Act
    result_stat = create_stat(stat_repo_mock, stat_type_repo_mock, stat_data)

    # Assert
    assert_stat_equal(result_stat, Stat(id=result_stat.id, **stat_data))
    stat_repo_mock.add.assert_called_once()


def test_get_stat_by_id(stat_repo_mock, stat):
    # Arrange
    stat_repo_mock.get.return_value = stat

    # Act
    result_stat = get_stat_by_id(stat_repo_mock, 1)

    # Assert
    assert_stat_equal(result_stat, stat)


def test_delete_stat_by_id(stat_repo_mock):
    # Arrange
    stat_repo_mock.get.return_value = Mock()  # Mock existing stat
    stat_repo_mock.delete = Mock()

    # Act
    delete_stat_by_id(stat_repo_mock, 1)

    # Assert
    stat_repo_mock.delete.assert_called_once_with(1)
