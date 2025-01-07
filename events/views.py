import logging
from rest_framework import viewsets, filters, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from .models import Event, User, Category, CustomUser as User, CustomUser
from .serializers import EventSerializer, UserSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from django.views.decorators.csrf import csrf_protect
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import get_user_model, logout, authenticate, login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import UserEditForm
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

User = get_user_model()

@login_required
def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_time = request.POST.get('date_time')
        location = request.POST.get('location')
        category_id = request.POST.get('category')
        capacity = request.POST.get('capacity')

        # Validation for required fields
        if not title or not date_time or not location:
            return render(request, 'events/create_event.html', {
                'categories': Category.objects.all(),
                'error': 'Title, Date & Time, and Location are required fields.'
            })

        # Convert date_time to an offset-aware datetime
        date_time = timezone.datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
        date_time = timezone.make_aware(date_time, timezone.get_current_timezone())

        # Prevent creating events with past dates
        if timezone.now() > date_time:
            return render(request, 'events/create_event.html', {
                'categories': Category.objects.all(),
                'error': 'Cannot create an event in the past.'
            })

        category = Category.objects.get(id=category_id)
        event = Event.objects.create(
            title=title,
            description=description,
            date_time=date_time,
            location=location,
            organizer=request.user,
            category=category,
            capacity=capacity,
        )
        return redirect('event-detail', event.id)
    
    categories = Category.objects.all()
    return render(request, 'events/create_event.html', {'categories': categories})

@login_required
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_time = request.POST.get('date_time')
        location = request.POST.get('location')
        category_id = request.POST.get('category')
        capacity = request.POST.get('capacity')

        # Validation for required fields
        if not title or not date_time or not location:
            return render(request, 'events/update_event.html', {
                'event': event,
                'categories': Category.objects.all(),
                'error': 'Title, Date & Time, and Location are required fields.'
            })

        # Convert date_time to an offset-aware datetime
        date_time = timezone.datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
        date_time = timezone.make_aware(date_time, timezone.get_current_timezone())

        # Prevent creating events with past dates
        if timezone.now() > date_time:
            return render(request, 'events/update_event.html', {
                'event': event,
                'categories': Category.objects.all(),
                'error': 'Cannot set an event date in the past.'
            })

        event.title = title
        event.description = description
        event.date_time = date_time
        event.location = location
        event.category_id = category_id
        event.capacity = capacity
        event.save()
        return redirect('profile')

    categories = Category.objects.all()
    return render(request, 'events/update_event.html', {'event': event, 'categories': categories})

@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('profile')  # Redirect to profile page after deleting
    return render(request, 'events/delete_event.html', {'event': event})

@login_required
def profile(request):
    user_events = request.user.events.all()
    registered_events = request.user.registered_events.all()
    return render(request, 'events/profile.html', {
        'user': request.user,
        'user_events': user_events,
        'registered_events': registered_events,
    })

def upcoming_events(request):
    events = Event.objects.filter(date_time__gte=timezone.now()).order_by('date_time')
    
    # Apply filters
    title = request.GET.get('title')
    if title:
        events = events.filter(title__icontains=title)
    
    location = request.GET.get('location')
    if location:
        events = events.filter(location__icontains=location)
    
    category = request.GET.get('category')
    if category:
        events = events.filter(category__name__icontains=category)
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        events = events.filter(date_time__range=[start_date, end_date])
    
    # Apply pagination
    paginator = Paginator(events, 10)  # 10 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'events/upcoming_events.html', {'events': page_obj})

def home(request):
    return render(request, 'events/home.html')

def event_list(request):
    events = Event.objects.all()  # Fetch events from DB
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'events/edit_profile.html', {'form': form})

@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    if user.is_new_user:
        user.is_new_user = False
        user.save()

@csrf_protect
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_new_user:
                return HttpResponseRedirect('/register/')
            else:
                return HttpResponseRedirect('/profile/')
        else:
            return render(request, 'events/login.html', {'error': 'Invalid credentials'})
    return render(request, 'events/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to homepage or any other page after logout

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category__name']
    search_fields = ['title', 'location']
    permission_classes = [AllowAny]  # Allow public access

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(date_time__gte=timezone.now())

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CustomPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed
    page_size_query_param = 'page_size'
    max_page_size = 100

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # Temporarily allow public access for testing
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['title', 'location', 'date_time', 'category__name']  # Added category__name
    ordering_fields = ['title', 'date_time']
    pagination_class = CustomPagination  # Added pagination

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

class EventManagementView(APIView):
    permission_classes = [IsAuthenticated]

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_register_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            user_data = serializer.validated_data
            user = CustomUser.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            # Authenticate and log in the user
            authenticated_user = authenticate(username=user_data['username'], password=user_data['password'])
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('home')
            else:
                return render(request, 'events/register.html', {'error': 'Authentication failed.'})
        return render(request, 'events/register.html', {'errors': serializer.errors})
    return render(request, 'events/register.html')
