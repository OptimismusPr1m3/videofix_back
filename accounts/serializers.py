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
        
    # def validate_my_videos(self, value):
    #     # Optional: Hier kannst du spezifische Validierungen für my_videos einfügen
    #     if not isinstance(value, list):
    #         raise serializers.ValidationError("my_videos must be a list.")
    #     return value

    # def validate_video_timestamps(self, value):
    #     # Optional: Validierungen für video_timestamps
    #     if not isinstance(value, list):
    #         raise serializers.ValidationError("video_timestamps must be a list.")
    #     for entry in value:
    #         if not isinstance(entry, dict) or 'URL' not in entry or 'STAMP' not in entry:
    #             raise serializers.ValidationError(
    #                 "Each entry in video_timestamps must be a dictionary with 'URL' and 'STAMP'."
    #             )
    #     return value