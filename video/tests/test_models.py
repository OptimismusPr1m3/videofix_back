import pytest
from datetime import date
from decimal import Decimal
from video.models import VideoItem


@pytest.mark.django_db
def test_video_item_creation():
    """Test the creation of a VideoItem object."""
    video = VideoItem.objects.create(
        title="Test Video",
        description="This is a test video.",
        genre="Action",
        rating=4.5,
        duration=Decimal('120.5678901234'),
    )
    assert video.title == "Test Video"
    assert video.description == "This is a test video."
    assert video.genre == "Action"
    assert video.rating == 4.5
    assert video.duration == Decimal('120.5678901234')
    assert video.released_at == date.today()
    assert video.created_at == date.today()
    assert not video.video_file  # video_file is None by default
    assert not video.cover_image  # cover_image is None by default


@pytest.mark.django_db
def test_video_item_str_representation():
    """Test the string representation of the VideoItem model."""
    video = VideoItem.objects.create(
        title="Test Video",
        description="This is a test video.",
        genre="Action"
    )
    assert str(video) == "Test Video"


@pytest.mark.django_db
def test_video_item_defaults():
    """Test the default values for fields in VideoItem."""
    video = VideoItem.objects.create(
        title="Default Test Video",
        description="This is a test video with default values.",
        genre="Drama",
    )
    assert video.rating == 1  # Default rating
    assert video.duration == Decimal('0')  # Default duration
    assert video.released_at == date.today()
    assert video.created_at == date.today()
    assert not video.video_file  # Default is None
    assert not video.cover_image  # Default is None


@pytest.mark.django_db
def test_video_item_file_uploads():
    """Test video_file and cover_image fields."""
    video = VideoItem.objects.create(
        title="File Test Video",
        description="Testing file uploads.",
        genre="Documentary",
        video_file="videos/test_video.mp4",
        cover_image="covers/test_image.jpg",
    )
    assert video.video_file.name == "videos/test_video.mp4"
    assert video.cover_image.name == "covers/test_image.jpg"
