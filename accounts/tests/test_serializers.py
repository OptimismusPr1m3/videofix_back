import pytest
from accounts.serializers import (
    MyUserSerializer, 
    MyUserChangeSerializer, 
    MyUserVideosChangeSerializer
)
from accounts.models import MyUser

@pytest.mark.django_db
def test_my_user_serializer_valid_data():
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
        first_name="Test",
        last_name="User",
        date_of_birth="1990-01-01",
        street="Test Street",
        street_number=123,
        zip_code="12345",
        city="Test City",
        country="Test Country",
        phone_number="1234567890"
    )
    serializer = MyUserSerializer(user)
    data = serializer.data

    # Assert serialized fields
    assert data['email'] == "testuser@example.com"
    assert data['first_name'] == "Test"
    assert data['last_name'] == "User"
    assert data['date_of_birth'] == "1990-01-01"
    assert data['street'] == "Test Street"
    assert data['street_number'] == 123
    assert data['zip_code'] == "12345"
    assert data['city'] == "Test City"
    assert data['country'] == "Test Country"
    assert data['phone_number'] == "1234567890"

@pytest.mark.django_db
def test_my_user_change_serializer_valid_data():
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
        first_name="OldFirstName",
        last_name="OldLastName"
    )
    data = {
        "first_name": "NewFirstName",
        "last_name": "NewLastName",
        "date_of_birth": "1985-01-01",
        "street": "New Street",
        "street_number": 456,
        "zip_code": "67890",
        "city": "New City",
        "country": "New Country",
        "phone_number": "9876543210",
    }
    serializer = MyUserChangeSerializer(user, data=data, partial=True)
    assert serializer.is_valid()
    serializer.save()

    # Assert updated fields
    user.refresh_from_db()
    assert user.first_name == "NewFirstName"
    assert user.last_name == "NewLastName"
    assert str(user.date_of_birth) == "1985-01-01"
    assert user.street == "New Street"
    assert user.street_number == 456
    assert user.zip_code == "67890"
    assert user.city == "New City"
    assert user.country == "New Country"
    assert user.phone_number == "9876543210"

@pytest.mark.django_db
def test_my_user_videos_change_serializer_valid_data():
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
    )
    data = {
        "my_videos": [{"video_id": "123", "name": "Test Video"}],
        "video_timestamps": {"123": 60},
    }
    serializer = MyUserVideosChangeSerializer(user, data=data, partial=True)
    assert serializer.is_valid()
    serializer.save()

    # Assert updated fields
    user.refresh_from_db()
    assert user.my_videos == [{"video_id": "123", "name": "Test Video"}]
    assert user.video_timestamps == {"123": 60}

@pytest.mark.django_db
def test_my_user_serializer_invalid_data():
    data = {
        "email": "not-an-email",
        "first_name": "Test",
        "last_name": "User",
        "date_of_birth": "invalid-date",
    }
    serializer = MyUserSerializer(data=data)
    assert not serializer.is_valid()
    assert "email" in serializer.errors
    assert "date_of_birth" in serializer.errors
