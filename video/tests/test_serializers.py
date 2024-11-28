import pytest
from decimal import Decimal
from datetime import date
from video.models import VideoItem
from video.serializers import VideoItemSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


@pytest.mark.django_db
def test_video_item_serializer_valid_data():
    """Test VideoItemSerializer with valid data."""
    
    # Erstelle ein korrektes Bild
    image_file = BytesIO()
    image = Image.new('RGB', (100, 100), color=(255, 255, 255))  # Ein einfaches weißes Bild
    image.save(image_file, 'JPEG')
    image_file.seek(0)
    
    mock_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
    mock_cover = SimpleUploadedFile("cover.jpg", image_file.read(), content_type="image/jpeg")

    video_data = {
        "title": "Test Video",
        "description": "This is a test video.",
        "released_at": date.today(),
        "genre": "Action",
        "created_at": date.today(),
        "video_file": mock_file,
        "cover_image": mock_cover,
        "rating": 4.5,
        "duration": Decimal("120.5678901234"),
    }

    serializer = VideoItemSerializer(data=video_data)
    assert serializer.is_valid(), serializer.errors

    video_item = serializer.save()
    assert video_item.title == video_data["title"]
    assert video_item.description == video_data["description"]
    assert video_item.released_at == video_data["released_at"]
    assert video_item.genre == video_data["genre"]
    assert video_item.video_file.name.startswith("videos/test_video")  # Nur den Präfix vergleichen
    assert video_item.cover_image.name.startswith("covers/cover")  # Nur den Präfix vergleichen
    assert video_item.rating == video_data["rating"]
    assert video_item.duration == video_data["duration"]


@pytest.mark.django_db
def test_video_item_serializer_missing_required_field():
    """Test VideoItemSerializer with missing required field."""
    video_data = {
        "description": "This is a test video without a title.",
        "genre": "Action",
    }

    serializer = VideoItemSerializer(data=video_data)
    assert not serializer.is_valid()
    assert "title" in serializer.errors  # Titel ist ein Pflichtfeld


@pytest.mark.django_db
def test_video_item_serializer_update():
    """Test VideoItemSerializer for updating an existing VideoItem."""
    mock_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")

    # Erstelle ein existierendes VideoItem
    video_item = VideoItem.objects.create(
        title="Old Title",
        description="Old Description",
        genre="Drama",
        rating=3.0,
        video_file=mock_file,
    )

    # Neue Daten für das Update
    updated_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "rating": 4.5,
    }

    serializer = VideoItemSerializer(instance=video_item, data=updated_data, partial=True)
    assert serializer.is_valid(), serializer.errors

    updated_video_item = serializer.save()
    assert updated_video_item.title == updated_data["title"]
    assert updated_video_item.description == updated_data["description"]
    assert updated_video_item.rating == updated_data["rating"]


@pytest.mark.django_db
def test_video_item_serializer_invalid_rating():
    """Test VideoItemSerializer with invalid rating value."""
    video_data = {
        "title": "Test Video",
        "description": "This video has an invalid rating.",
        "genre": "Action",
        "rating": "Invalid Rating",  # Ungültiger Wert
    }

    serializer = VideoItemSerializer(data=video_data)
    assert not serializer.is_valid()
    assert "rating" in serializer.errors
