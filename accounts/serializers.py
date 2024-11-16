from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import MyUser


# class MyUserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = MyUser
#         fields = ['email', 'first_name', 'last_name']


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'date_of_birth', 'date_joined', 'street', 'street_number', 'zip_code', 'city', 'country', 'phone_number', 'my_videos', 'video_timestamps')

class MyUserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'date_of_birth', 'street', 'street_number', 'zip_code', 'city', 'country', 'phone_number')


class MyUserVideosChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('my_videos','video_timestamps',)