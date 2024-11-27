import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import VideoItem
from accounts.models import MyUser
from urllib.parse import urljoin
from django.core.cache import cache



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

    cache.clear()

    # generates api url from video id (:
    # local urlstring ->http://127.0.0.1:8000/api/videos/
    video_api_url = urljoin(f"https://storage.bastian-wolff.com/api/videos/", f"{instance.id}/")
    print(f"Zu entfernende Video-URL: {video_api_url}")

    # filters users with timestamps, users without timestamps will be ignored
    users = MyUser.objects.filter(video_timestamps__isnull=False)
    for user in users:
        if user.video_timestamps:
            print(f"Überprüfe Benutzer {user.email}, Zeitstempel: {user.video_timestamps}")

            # updates the timestamps and saves updated stamp to user
            updated_timestamps = [
                entry for entry in user.video_timestamps if entry.get("URL") != video_api_url
            ]

            if len(updated_timestamps) != len(user.video_timestamps):
                user.video_timestamps = updated_timestamps
                user.save()
                print(f"Video {video_api_url} aus Zeitstempeln von Benutzer {user.email} entfernt.")















