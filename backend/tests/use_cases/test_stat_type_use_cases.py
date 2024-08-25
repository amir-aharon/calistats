from calistats.domain.repositories import StatTypeRepository
import pytest
from unittest.mock import Mock
from calistats.domain.models import StatType
from calistats.application.stat_type_use_cases import create_stat_type, get_stat_type_by_id, delete_stat_type_by_id


@pytest.fixture
def stat_type_repo_mock():
    return Mock()


@pytest.fixture
def stat_type_data():
    return {"name": "Strength", "unit": "kg"}


@pytest.fixture
def stat_type():
    return StatType(id=1, name="Strength", unit="kg")


def test_create_stat_type(stat_type_repo_mock, stat_type_data):
    # Arrange
    stat_type_repo_mock.add = Mock()
    stat_type_repo_mock.get.return_value = stat_type_data

    # Act
    result_stat_type = create_stat_type(stat_type_repo_mock, stat_type_data)

    # Assert
    assert {**result_stat_type} == {**stat_type_data}
    stat_type_repo_mock.add.assert_called_once()


def test_get_stat_type_by_id(stat_type_repo_mock: Mock, stat_type: StatType):
    # Arrange
    stat_type_repo_mock.get.return_value = stat_type

    # Act
    result_stat_type = get_stat_type_by_id(stat_type_repo_mock, 1)

    # Assert
    assert {**result_stat_type.__dict__} == {**stat_type.__dict__}


def test_delete_stat_type_by_id(stat_type_repo_mock: Mock):
    # Arrange
    stat_type_repo_mock.get.return_value = Mock()  # Mock existing stat type
    stat_type_repo_mock.delete = Mock()

    # Act
    delete_stat_type_by_id(stat_type_repo_mock, 1)

    # Assert
    stat_type_repo_mock.delete.assert_called_once_with(1)
