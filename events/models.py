from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='events_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='events_user_set', blank=True)
    
class CustomUser(AbstractUser):
    is_new_user = models.BooleanField(default=True)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events')  # Ensure related_name is set
    capacity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    registered_users = models.ManyToManyField(CustomUser, related_name='registered_events')

    def __str__(self):
        return self.title

    def is_full(self):
        return self.registered_users.count() >= self.capacity
