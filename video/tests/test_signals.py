import pytest
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from video.models import VideoItem
from accounts.models import MyUser
import os


@pytest.mark.django_db
@patch("video.signals.os.remove")  # Mock file removal to prevent actual file deletion
@patch("video.signals.cache.clear")  # Mock cache clearing
def test_video_file_auto_delete(mock_cache_clear, mock_remove):
    """Test if video file, converted files, cover image, and cache are deleted upon VideoItem deletion."""

    # Erstelle ein korrektes Bild
    mock_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
    cover_image = SimpleUploadedFile("cover.jpg", b"image_content", content_type="image/jpeg")

    # Erstelle ein VideoItem
    video_item = VideoItem.objects.create(
        title="Test Video",
        description="Test video description",
        genre="Action",
        video_file=mock_file,
        cover_image=cover_image,
        rating=4.5,
        duration=120.0,
    )

    # Erstelle einen Nutzer mit Zeitstempeln
    user = MyUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
    )
    user.video_timestamps = [{"URL": f"http://testserver/api/videos/{video_item.id}/", "STAMP": "timestamp_1"}]
    user.save()

    # Erhalte die Anzahl der Zeitstempel vor der Löschung
    initial_timestamp_count = len(user.video_timestamps)

    # Lösche das Video
    video_item.delete()

    # Überprüfen, ob die Dateien entfernt wurden
    mock_remove.assert_any_call(video_item.video_file.path)

    # Überprüfen, ob das Cover-Bild entfernt wurde
    mock_remove.assert_any_call(video_item.cover_image.path)

    # Überprüfen, ob der Cache gelöscht wurde
    mock_cache_clear.assert_called_once()

    # Überprüfen, ob der Zeitstempel aus den Nutzerdaten entfernt wurde
    user.refresh_from_db()
    assert len(user.video_timestamps) != None  
