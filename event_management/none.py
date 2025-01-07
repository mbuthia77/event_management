from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, authenticate
from django.utils import timezone
from .models import Event, CustomUser
from .serializers import EventSerializer, UserSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # Temporarily allow public access for testing
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['title', 'location', 'date_time', 'category__name']
    ordering_fields = ['title', 'date_time']
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset.filter(date_time__gte=timezone.now())
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date_time__range=[start_date, end_date])
        return queryset

    def perform_create(self, serializer):
        event = serializer.save(organizer=self.request.user)
        if event.is_full():
            raise serializers.ValidationError("Event capacity has been reached")

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        upcoming_events = Event.objects.filter(date_time__gte=timezone.now()).order_by('date_time')
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()
        if event.is_full():
            return Response({"detail": "Event is full."}, status=400)
        event.registered_users.add(request.user)
        return render(request, 'events/success_registration.html', {'event': event})

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_register_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])  # Set password correctly
            user.save()

            # Print debug statements to check data flow
            print("User created: ", user.username)
            print("Validating data: ", serializer.validated_data)

            # Authenticate and log in the user
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user is not None:
                print("User authenticated successfully")
                login(request, user)
                return redirect('home')
            else:
                print("Authentication failed")
                return render(request, 'events/register.html', {'error': 'Authentication failed.'})
        else:
            print("Serializer errors: ", serializer.errors)
        return render(request, 'events/register.html', {'errors': serializer.errors})
    return render(request, 'events/register.html')

