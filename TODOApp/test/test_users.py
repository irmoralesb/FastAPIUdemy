from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/users/user_info")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'irmorales'
    assert response.json()['first_name'] == 'Raul'
    assert response.json()['last_name'] == 'Morales'
    assert response.json()['role'] == 'admin'


def test_change_password_success(test_user):
    response = client.put("/users/change_password",
                          json={'old_password': '123456!', 'new_password': '123456@', 'new_password_repeat': '123456@'})
    assert response.status_code == status.HTTP_200_OK


def test_change_password_invalid_password(test_user):
    response = client.put("/users/change_password",
                          json={'old_password': '123456$', 'new_password': '123456@', 'new_password_repeat': '123456@'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_change_password_passwords_dont_match(test_user):
    response = client.put("/users/change_password",
                          json={'old_password': '123456!', 'new_password': '123456@', 'new_password_repeat': '123456#'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
