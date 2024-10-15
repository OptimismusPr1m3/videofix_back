from rest_framework import viewsets, status
from video.models import VideoItem
from video.serializers import VideoItemSerializer
from rest_framework.permissions import IsAuthenticated
from video.tasks import convert_480p
# Create your views here.

'class LoginView():'


class VideoViewSet(viewsets.ModelViewSet):
    queryset = VideoItem.objects.all()
    serializer_class = VideoItemSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        video_item = serializer.save()
        convert_480p.delay(video_item.video_file.path)
        print('Geil', video_item)
        return Response(
            {'message': 'Video uploaded successfully! Conversion in progress...'},
            status=status.HTTP_201_CREATED
        )


