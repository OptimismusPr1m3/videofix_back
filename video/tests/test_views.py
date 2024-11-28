import pytest
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import MyUser
from rest_framework.authtoken.models import Token
from video.models import VideoItem
from django.core.cache import cache
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch


@pytest.mark.django_db
def test_video_list_view_authenticated_user():
    """Test listing videos as an authenticated user."""
    client = APIClient()
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
    )
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    # Erstelle VideoItems
    VideoItem.objects.create(
        title="Video 1",
        description="Test description 1",
        genre="Action",
        rating=4.5,
    )
    VideoItem.objects.create(
        title="Video 2",
        description="Test description 2",
        genre="Drama",
        rating=5.0,
    )

    # Anfrage an die Video-Liste
    response = client.get("/api/videos/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2  # Zwei Videos sollten zurückgegeben werden


@pytest.mark.django_db
def test_video_create_view_authenticated_user(mocker):
    client = APIClient()
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
    )
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    mocker.patch("video.tasks.convert_480p_with_thumbnail.delay")

    mock_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
    data = {
        "title": "New Video",
        "description": "New video description",
        "genre": "Documentary",
        "rating": 4.2,
        "duration": Decimal("120.1234567890"),
        "video_file": mock_file,
    }

    response = client.post("/api/videos/", data=data, format="multipart")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data.get("url") is not None  # URL des neuen Videos überprüfen



@pytest.mark.django_db
def test_video_update_view_authenticated_user(mocker):
    # Client und Authentifizierung
    client = APIClient()
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
    )
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    # Mock Celery Task
    mocker.patch("video.tasks.convert_480p_with_thumbnail.delay")

    # Datei erstellen und überprüfen
    mock_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
    print("File Name:", mock_file.name, "File Size:", mock_file.size)  # Debug: Name und Größe überprüfen

    # VideoItem erstellen
    video = VideoItem.objects.create(
        title="Old Title",
        description="Old description",
        genre="Drama",
        rating=3.0,
        duration=Decimal("120.1234567890"),
        video_file=mock_file,
    )

    # Daten für das Update
    updated_file = SimpleUploadedFile("updated_video.mp4", b"updated_content", content_type="video/mp4")
    data = {
        "title": "Updated Title",
        "description": "Updated description",
        "rating": 4.5,
        "genre": video.genre,
        "duration": str(video.duration),  # `duration` als String übergeben
        "video_file": updated_file,  # Neues File für Update
    }

    # PUT-Anfrage zum Aktualisieren des Videos
    response = client.put(f"/api/videos/{video.id}/", data=data, format="multipart")

    # Debugging: Fehlerdetails ausgeben, falls der Status nicht 200 ist
    if response.status_code == 400:
        print("Response Errors:", response.data)

    # Überprüfen, ob die Anfrage erfolgreich war
    assert response.status_code == status.HTTP_200_OK

    # Datenbank erneut abfragen und prüfen, ob die Werte aktualisiert wurden
    video.refresh_from_db()
    assert video.title == "Updated Title"
    assert video.description == "Updated description"
    assert video.rating == 4.5
    assert video.video_file.name.endswith("updated_video.mp4")  # Dateiname prüfen



@pytest.mark.django_db
def test_cache_clearing_on_update(mocker):
    client = APIClient()
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
    )
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    video = VideoItem.objects.create(
        title="Cached Video",
        description="Old description",
        genre="Action",
        rating=3.5,
    )

    cache_key = "video_list"
    cache.set(cache_key, {"title": video.title, "description": video.description})
    cached_data = cache.get(cache_key)
    assert cached_data is not None
    
    mock_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
     
    data = {
        "title": "Updated Cached Video",
        "description": "Updated description",
        "genre": video.genre,  # Falls erforderlich
        "rating": video.rating,  # Falls erforderlich
        "video_file": mock_file,
    }
    response = client.put(f"/api/videos/{video.id}/", data=data, format="multipart")
    assert response.status_code == status.HTTP_200_OK

    cached_data = cache.get(cache_key)
    assert cached_data is None



@pytest.mark.django_db
@patch("video.views.cache_page", lambda x: x)
def test_video_list_view_caching(mocker):
    """Test caching for video list view."""
    client = APIClient()
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
    )
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    # Erstelle VideoItems
    VideoItem.objects.create(
        title="Video 1",
        description="Test description 1",
        genre="Action",
        rating=4.5,
    )
    VideoItem.objects.create(
        title="Video 2",
        description="Test description 2",
        genre="Drama",
        rating=5.0,
    )

    # Erste Anfrage sollte den Cache setzen
    response = client.get("/api/videos/")
    assert response.status_code == status.HTTP_200_OK
