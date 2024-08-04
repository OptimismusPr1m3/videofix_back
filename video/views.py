from rest_framework import viewsets, status
from video.models import VideoItem
from video.serializers import VideoItemSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

'class LoginView():'


class VideoViewSet(viewsets.ModelViewSet):
    queryset = VideoItem.objects.all()
    serializer_class = VideoItemSerializer
    permission_classes = (IsAuthenticated,)


