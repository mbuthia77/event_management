from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Event
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)


