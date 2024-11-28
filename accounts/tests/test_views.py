import pytest
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import MyUser
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_my_user_me_view_authenticated_user():
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
    )
    client = APIClient()
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = client.get("/api/accounts/users/me/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_my_user_me_view_unauthenticated_user():
    client = APIClient()
    response = client.get("/api/accounts/users/me/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_my_user_me_change_post_authenticated_user():
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
    )
    client = APIClient()
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    data = {"first_name": "UpdatedFirstName"}
    response = client.post("/api/accounts/users/me/change/", data=data)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.first_name == "UpdatedFirstName"


@pytest.mark.django_db
def test_my_user_me_change_post_unauthenticated_user():
    client = APIClient()
    data = {"first_name": "UpdatedFirstName"}
    response = client.post("/api/accounts/users/me/change/", data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_my_user_me_change_patch_authenticated_user():
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
        my_videos=[]
    )
    client = APIClient()
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    data = {"my_videos": [{"video_id": "123", "name": "Test Video"}]}
    response = client.patch("/api/accounts/users/me/change/", data=data, format="json")
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.my_videos == [{"video_id": "123", "name": "Test Video"}]


@pytest.mark.django_db
def test_custom_login_view_valid_credentials():
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
    )
    user.is_verified = True
    user.is_active = True
    user.save()

    client = APIClient()
    data = {"email": "testuser@example.com", "password": "securepassword123"}
    response = client.post("/api/accounts/auth/login/", data=data)

    print(response.data)  # Debugging-Ausgabe
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data  # Überprüfe, ob ein Token zurückgegeben wird



@pytest.mark.django_db
def test_custom_login_view_invalid_credentials():
    MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
    )
    client = APIClient()
    data = {"email": "testuser@example.com", "password": "wrongpassword"}
    response = client.post("/api/accounts/auth/login/", data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["detail"] == "Unable to login with provided credentials."


@pytest.mark.django_db
def test_custom_login_view_unverified_user():
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
    )
    client = APIClient()
    data = {"email": "testuser@example.com", "password": "securepassword123"}
    response = client.post("/api/accounts/auth/login/", data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["detail"] == "User account not verified."
