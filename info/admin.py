from django.contrib import admin
from .models import Profile, Location, ContactMessage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    The view on the admin site for the Profile model
    """
    list_display = ('first_name', 'last_name', 'job_title', 'created_on')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    The view on the admin site for the Location model
    """
    list_display = ('name', 'street_name', 'city', 'created_on')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    The view on the admin site for messages sent through the contact form
    """
    list_display = ('subject', 'name', 'email', 'created_on', 'handled')
    list_filter = ('handled',)
    list_editable = ('handled',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_on')
