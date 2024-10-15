from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import MyUserSerializer, MyUserChangeSerializer, MyUserVideosChangeSerializer


class MyUserMe(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MyUserSerializer

    def get(self, request, format=None):
        print("MyUserMe view called")
        return Response(self.serializer_class(request.user).data)


class MyUserMeChange(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MyUserChangeSerializer
    serializ_class = MyUserVideosChangeSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user

            if 'first_name' in serializer.data:
                user.first_name = serializer.data['first_name']
            if 'last_name' in serializer.data:
                user.last_name = serializer.data['last_name']
            if 'date_of_birth' in serializer.data:
                user.date_of_birth = serializer.data['date_of_birth']
            if 'street' in serializer.data:
                user.street = serializer.data['street']
            if 'street_number' in serializer.data:
                user.street_number = serializer.data['street_number']
            if 'zip_code' in serializer.data:
                user.zip_code = serializer.data['zip_code']
            if 'city' in serializer.data:
                user.city = serializer.data['city']
            if 'country' in serializer.data:
                user.country = serializer.data['country']
            if 'phone_number' in serializer.data:
                user.phone_number = serializer.data['phone_number']
            if 'my_videos' in serializer.data:
                user.my_videos = serializer.data['my_videos']

            user.save()

            content = {'success': _('User information changed.')}
            return Response(content, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        serializer = self.serializ_class(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            
            if 'my_videos' in serializer.data:
                user.my_videos = serializer.data['my_videos']
                
            user.save()
            
            content = {'success': _('User information for Videos changed.')}
            return Response(content, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
