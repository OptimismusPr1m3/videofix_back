from celery import shared_task
import os
import subprocess
import logging
from django.conf import settings
from video.models import VideoItem

logger = logging.getLogger(__name__)

@shared_task
def convert_480p_with_thumbnail(video_item_id, source):
    logger.info(f'Starting conversion for {source}')
    base,ext = os.path.splitext(source)
    target_video = f'{base}_480p{ext}'
    
    thumbnail_dir = os.path.join('media', 'covers')
    os.makedirs(thumbnail_dir, exist_ok=True)
    
    thumbnail = os.path.join(thumbnail_dir, f'{os.path.basename(base)}_thumbnail.png')
    
    # commands for video convert + thumbnail generation
    video_cmd = ['ffmpeg', '-i', source, '-s', 'hd480', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-strict', '-2', target_video]
    thumbnail_cmd = ['ffmpeg', '-i', source, '-ss', '00:00:01', '-frames:v', '1', '-vf', 'scale=1280:720', '-update', '1', thumbnail]
    
    try:
        subprocess.run(video_cmd, capture_output=True, check=True)
        logger.info(f'Conversion completed for {source}')
        
        subprocess.run(thumbnail_cmd, capture_output=True, check=True)
        logger.info(f'Thumbnail generated for {source}: {thumbnail}')
        
        video_item = VideoItem.objects.get(id=video_item_id)
        video_item.cover_image.name = os.path.relpath(thumbnail, settings.MEDIA_ROOT)
        video_item.save()
        
        return {
            'video_480p': target_video,
            'thumbnail': thumbnail
        }
        
    except subprocess.CalledProcessError as e:
        logger.error(f'Conversion failed for {source}: {e.stderr}')





def convert_720p(source):
    base, ext = os.path.splitext(source)
    target = f'{base}_720p{ext}'
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    #run = subprocess.run(cmd)
    
    try:
        result = subprocess.run(cmd, capture_output=True, check=True)
        logger.info(f'Conversion completed for {source}: {result.stdout}')
    except subprocess.CalledProcessError as e:
        logger.error(f'Conversion failed for {source}: {e.stderr}')


