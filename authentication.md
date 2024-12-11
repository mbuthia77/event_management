# Authentication Setup

## Introduction
This document describes how to secure the Event Management API using JWT authentication with Django REST Framework and Simple JWT.

## Installation
1. First, install the necessary packages:

$ pip install djangorestframework djangorestframework-simplejwt

2. Update settings.py
Add the necessary settings for Django REST Framework and Simple JWT

# settings.py

INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

3. Create Views for Token Authentication
Add views for obtaining and refreshing tokens in event_management/urls.py:
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events.views import EventViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'events', EventViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

4. Test the Authentication
Use Postman to test the authentication setup.

Obtain a Token
URL: http://localhost:8000/api/token/ Method: POST Body:
json
{
    "username": "your_username",
    "password": "your_password"
}

Response
{
    "access": "your_access_token",
    "refresh": "your_refresh_token"
}

Use the Token
Include the obtained token in the Authorization header for subsequent requests.