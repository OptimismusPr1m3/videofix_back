import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import VideoItem




@receiver(post_save, sender=VideoItem)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    
    if created:
        print('New Video created !')
        
@receiver(post_delete, sender=VideoItem)
def video_file_auto_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            print('Video wurde geloescht')
            
    if instance.cover_image:
        if os.path.isfile(instance.cover_image.path):
            os.remove(instance.cover_image.path)
            print('Cover wurde geloescht')

























































