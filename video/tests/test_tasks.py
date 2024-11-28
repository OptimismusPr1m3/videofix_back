
import os
import pytest
from unittest.mock import patch
from video.tasks import convert_480p_with_thumbnail
from video.models import VideoItem
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache

@pytest.mark.django_db
@patch("video.tasks.subprocess.run")  # Mock subprocess to prevent actual ffmpeg call
@patch("video.tasks.cache.clear")  # Mock cache clearing
def test_convert_480p_with_thumbnail(mock_cache_clear, mock_subprocess_run):
    # Create a video item
    mock_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
    video_item = VideoItem.objects.create(
        title="Test Video",
        description="A test video",
        genre="Action",
        rating=4.5,
        video_file=mock_file
    )
    
    video_item_id = video_item.id
    video_file_path = video_item.video_file.path
    
    # Mock the subprocess to prevent actually running ffmpeg
    mock_subprocess_run.return_value = None  # Simulate successful subprocess execution

    # Run the task
    convert_480p_with_thumbnail(video_item_id, video_file_path)

    # Check if subprocess was called (video conversion and thumbnail generation)
    assert mock_subprocess_run.call_count == 2  # video conversion and thumbnail generation
    assert mock_subprocess_run.call_args_list[0][0][0] == ['ffmpeg', '-i', video_file_path, '-s', 'hd480', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-strict', '-2', f'{os.path.splitext(video_file_path)[0]}_480p{os.path.splitext(video_file_path)[1]}']


    # Ensure the video item was updated
    video_item.refresh_from_db()
    assert video_item.cover_image.name.endswith("_thumbnail.png")

    # Ensure the cache was cleared
    mock_cache_clear.assert_called_once()
