from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Event, Category

# Registering models
admin.site.register(Event)
admin.site.register(Category)

# Unregister default CustomUser model if already registered
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass

# Custom UserAdmin
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

# Register CustomUser with CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
