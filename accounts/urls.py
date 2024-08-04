from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import MyUserMe, MyUserMeChange


urlpatterns = [
    path('users/me/', MyUserMe.as_view(), name='user-me'),
    path('users/me/change/', MyUserMeChange.as_view(), name='user-me-change'),
]


