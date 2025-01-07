"""
URL configuration for event_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from events.views import profile, logout_view, home, event_list, event_detail, upcoming_events, custom_login_view, create_event, update_event, delete_event, user_register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('events.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('profile/', profile, name='profile'),
    #path('register/', register, name='user-register'),
    path('register/', user_register_view, name='user_register'),
    path('events/', event_list, name='event-list'),
    path('events/<int:event_id>/', event_detail, name='event-detail'),
    path('upcoming-events/', upcoming_events, name='upcoming-events'),
    path('login/', custom_login_view, name='login'),
    path('', home, name='home'),
    path('create-event/', create_event, name='create-event'),
    path('update-event/<int:pk>/', update_event, name='event-update'), # URL for updating events 
    path('delete-event/<int:pk>/', delete_event, name='event-delete'), # URL for deleting events
    path('logout/', logout_view, name='logout'), # Add the logout path
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
