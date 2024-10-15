from celery import shared_task
import os
import subprocess
import logging

logger = logging.getLogger(__name__)

@shared_task
def convert_480p(source):
    logger.info(f'Starting conversion for {source}')
    base,ext = os.path.splitext(source)
    target = f'{base}_480p{ext}'
    cmd = ['ffmpeg', '-i', source, '-s', 'hd480', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-strict', '-2', target]
    
    try:
        result = subprocess.run(cmd, capture_output=True, check=True)
        logger.info(f'Conversion completed for {source}: {result.stdout}')
    except subprocess.CalledProcessError as e:
        logger.error(f'Conversion failed for {source}: {e.stderr}')

def convert_720p(source):
    base, ext = os.path.splitext(source)
    target = f'{base}_720p{ext}'
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    run = subprocess.run(cmd)
