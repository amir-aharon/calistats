import pytest
from unittest.mock import Mock
from calistats.domain.models import User
from calistats.application.user_use_cases import create_user, get_user_by_id, get_user_by_email, delete_user_by_id


@pytest.fixture
def user_repo_mock():
    return Mock()


@pytest.fixture
def user_data():
    return {"name": "John Doe", "email": "john.doe@example.com", "password": "securepassword"}


@pytest.fixture
def user():
    return User(id=1, name="John Doe", email="john.doe@example.com", password="securepassword")


def test_create_user(user_repo_mock, user_data):
    # Arrange
    user_repo_mock.add = Mock()

    # Act
    result_user = create_user(user_repo_mock, user_data)

    # Assert
    assert result_user.name == user_data["name"]
    assert result_user.email == user_data["email"]
    assert result_user.password == user_data["password"]
    user_repo_mock.add.assert_called_once()


def test_get_user_by_id(user_repo_mock, user):
    # Arrange
    user_repo_mock.get.return_value = user

    # Act
    result_user = get_user_by_id(user_repo_mock, 1)

    # Assert
    assert result_user.id == user.id
    assert result_user.name == user.name
    assert result_user.email == user.email
    assert result_user.password == user.password


def test_get_user_by_email(user_repo_mock, user):
    # Arrange
    user_repo_mock.get_by_email.return_value = user

    # Act
    result_user = get_user_by_email(user_repo_mock, "john.doe@example.com")

    # Assert
    assert result_user.id == user.id
    assert result_user.name == user.name
    assert result_user.email == user.email
    assert result_user.password == user.password


def test_delete_user_by_id(user_repo_mock):
    # Arrange
    user_repo_mock.get.return_value = Mock()  # Mock existing user
    user_repo_mock.delete = Mock()

    # Act
    delete_user_by_id(user_repo_mock, 1)

    # Assert
    user_repo_mock.delete.assert_called_once_with(1)
