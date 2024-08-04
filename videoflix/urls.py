"""
URL configuration for videoflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from . import views
from video.views import VideoViewSet
from videoflix.views import UserViewSet

router = DefaultRouter()
router.register(r'videos', VideoViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/accounts/', include('accounts.urls')),
    path('api/accounts/', include('authemail.urls')),
    path('signup/verify/', views.SignUpVerifyFE.as_view()),
    path('signup/verified/', views.SignUpVerifiedFE.as_view(), name='signup_verified_page'),
    path('signup/not_verified/', views.SignUpNotVerifiedFE.as_view(), name='signup_not_verified_page'),
    path('password/reset/verify/', views.PasswordResetVerifyFE.as_view()),
    path('password/reset/verified/', views.PasswordResetVerifiedFE.as_view(), name='password_reset_verified_page'),
    path('password/reset/not_verified/', views.PasswordResetNotVerifiedFE.as_view(), name='password_reset_not_verified_page'),
    path('password/reset/success/', views.PasswordResetSuccessFrontEnd.as_view(),
         name='password_reset_success_page'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
