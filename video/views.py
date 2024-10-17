from rest_framework.response import Response  # Anstelle von requests.Response
from rest_framework import viewsets, status
from video.models import VideoItem
from video.serializers import VideoItemSerializer
from rest_framework.permissions import IsAuthenticated
from video.tasks import convert_480p
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
# Create your views here.

'class LoginView():'


class VideoViewSet(viewsets.ModelViewSet):
    queryset = VideoItem.objects.all().order_by('-released_at')
    serializer_class = VideoItemSerializer
    permission_classes = (IsAuthenticated,)
    
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer_class):
        print("Jetzt wirds vermutlich gespeichert !")
        if 3 == 3:
            print("ja genau !")
        video_item = serializer_class.save()
        convert_480p.delay(video_item.video_file.path)
        print('Geil', video_item)
        return Response(
            {'message': 'Video uploaded successfully! Conversion in progress...'},
            status=status.HTTP_201_CREATED
        )


