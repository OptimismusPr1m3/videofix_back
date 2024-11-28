from rest_framework.response import Response  # Anstelle von requests.Response
from rest_framework import viewsets, status
from video.models import VideoItem
from video.serializers import VideoItemSerializer
from rest_framework.permissions import IsAuthenticated
from video.tasks import convert_480p_with_thumbnail
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache


class VideoViewSet(viewsets.ModelViewSet):
    queryset = VideoItem.objects.all().order_by('-released_at')
    serializer_class = VideoItemSerializer
    permission_classes = (IsAuthenticated,)
    
    @method_decorator(cache_page(60 * 15, key_prefix="video_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer_class):
        video_item = serializer_class.save()
        video_path = video_item.video_file.path
        convert_480p_with_thumbnail.delay(video_item.id, video_path)

        #cache_key = f"video_list:{self.request.path}"
        cache.clear()

        print('Geil', video_item)
        return Response(
            {'message': 'Video uploaded successfully! Conversion in progress...'},
            status=status.HTTP_201_CREATED
        )
    def perform_update(self, serializer):
        print('Videodetails been actualized !')
        video_item = serializer.save()
        cache.clear()
        print('Cache cleared')
        return Response(
            {'message': 'Video details updated successfully!'},
            status=status.HTTP_200_OK)


