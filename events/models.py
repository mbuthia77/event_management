from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='events_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='events_user_set', blank=True)


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def is_full(self): 
        return self.attendees.count() >= self.capacity

    def __str__(self):
        return self.title
