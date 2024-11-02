from datetime import date
from django.db import models

# Create your models here.

class VideoItem(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    released_at = models.DateField(default=date.today)
    genre = models.CharField(max_length=20)
    created_at = models.DateField(default=date.today)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers', blank=True, null=True)
    rating = models.FloatField(default=1)
    duration = models.DecimalField(max_digits=20, decimal_places=10,default=0, blank=True, null=True)

    def __str__(self):
        return self.title
