from rest_framework import serializers

from accounts.models import MyUser


class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name']