from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, UserViewSet, user_register_view, profile, logout_view, update_event, delete_event, home, event_list, event_detail, upcoming_events, custom_login_view, edit_profile, create_event, CategoryList, CategoryDetail #UserCreateView

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('', include(router.urls)),
    path('event-list/', event_list, name='event-list'),
    path('events/<int:pk>/', event_detail, name='event-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'), 
    #path('register/', UserCreateView.as_view(), name='user-register'),
    path('register/', user_register_view, name='user_register'),
    path('profile/', profile, name='profile'),
    path('upcoming-events/', upcoming_events, name='upcoming-events'),
    path('login/', custom_login_view, name='login'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('create-event/', create_event, name='create-event'),  # Ensure this line is included
    path('update-event/<int:pk>/', update_event, name='event-update'), # URL for updating events 
    path('delete-event/<int:pk>/', delete_event, name='event-delete'), # URL for deleting events
    path('logout/', logout_view, name='logout'), # Add the logout path
]
