from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

from video.models import VideoItem
from video.serializers import UserRegistrationSerializer, UserSerializer, VideoItemSerializer

# Create your views here.

'class LoginView():'


class VideoViewSet(viewsets.ModelViewSet):
    queryset = VideoItem.objects.all()
    serializer_class = VideoItemSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        if request.method == 'POST':
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response( {
                    'first_name': user.first_name,
                    'email': user.email,
                    'last_name': user.last_name,
                }, status=status.HTTP_201_CREATED)