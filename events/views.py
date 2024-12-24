import logging
from rest_framework import viewsets, filters, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Event, User
from .serializers import EventSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['title', 'location', 'date']
    ordering_fields = ['title', 'date']

    def get_queryset(self):
        user = self.request.user
        logger.info(f"User: {user}, Type: {type(user)}")
        if isinstance(user, User):
            logger.info("User is a valid User instance")
            queryset = self.queryset.filter(user=user)
            logger.info(f"Queryset: {queryset}")
            queryset = queryset.filter(date__gte=timezone.now())
            title = self.request.query_params.get('title')
            if title is not None:
                queryset = queryset.filter(title__icontains=title)
            location = self.request.query_params.get('location')
            if location is not None:
                queryset = queryset.filter(location__icontains=location)
            start_date = self.request.query_params.get('start_date')
            end_date = self.request.query_params.get('end_date')
            if start_date is not None and end_date is not None:
                queryset = queryset.filter(date__range=[start_date, end_date])
            return queryset
        else:
            logger.error("User is not an instance of User model")
            raise ValueError("User is not an instance of User model")

    def perform_create(self, serializer):
        event = serializer.save(user=self.request.user)
        if event.is_full():
            raise serializers.ValidationError("Event capacity has been reached")

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)

