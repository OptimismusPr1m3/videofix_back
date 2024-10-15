import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import VideoItem
from video.tasks import convert_480p, convert_720p




@receiver(post_save, sender=VideoItem)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    
    if created:
        print('New Video created !')
        convert_480p(instance.video_file.path)
        ##convert_720p(instance.video_file.path)
        
@receiver(post_delete, sender=VideoItem)
def video_file_auto_delete(sender, instance, **kwargs):
    if instance.video_file:
        original_file_path = instance.video_file.path
        if os.path.isfile(original_file_path):
            os.remove(original_file_path)
            print('Video wurde geloescht', original_file_path)
                
        base, ext = os.path.splitext(original_file_path)
        converted_file_path_480 = f'{base}_480p{ext}'
        converted_file_path_720 = f'{base}_720p{ext}'
        if os.path.isfile(converted_file_path_480):
            os.remove(converted_file_path_480)
            print('Konvertiertes Video geloescht', converted_file_path_480)
        if os.path.isfile(converted_file_path_720):
            os.remove(converted_file_path_720)
            print('Konvertiertes Video geloescht', converted_file_path_720)
            
    if instance.cover_image:
        if os.path.isfile(instance.cover_image.path):
            os.remove(instance.cover_image.path)
            print('Cover wurde geloescht')

























































