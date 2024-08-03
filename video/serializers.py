from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import MyUser
from .models import VideoItem

class VideoItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VideoItem
        fields = '__all__'



                  