import os
import subprocess

def convert_480p(source):
    base,ext = os.path.splitext(source)
    target = f'{base}_480p{ext}'
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    run = subprocess.run(cmd)
    
def convert_720p(source):
    base, ext = os.path.splitext(source)
    target = f'{base}_720p{ext}'
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    run = subprocess.run(cmd)