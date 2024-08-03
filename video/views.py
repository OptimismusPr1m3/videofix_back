from rest_framework import viewsets, status
from video.models import VideoItem
from video.serializers import VideoItemSerializer

# Create your views here.

'class LoginView():'


class VideoViewSet(viewsets.ModelViewSet):
    queryset = VideoItem.objects.all()
    serializer_class = VideoItemSerializer


