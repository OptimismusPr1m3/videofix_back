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
        fields = ('id', 'email', 'first_name', 'last_name', 'date_of_birth')


class MyUserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'date_of_birth')