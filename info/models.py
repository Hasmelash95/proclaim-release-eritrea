from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    """
    Profile model for info page.
    """
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    image = CloudinaryField('image', default='temporary')
    job_title = models.CharField(max_length=30, default='Volunteer')
    about = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.first_name + self.last_name


class Location(models.Model):
    """
    Location model for info page.
    """
    name = models.CharField(max_length=60)
    street_name = models.CharField(max_length=60)
    city = models.CharField(max_length=20)
    post_code = models.CharField(max_length=10)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    """
    Message sent through the contact form, read by staff in the admin.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    handled = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.subject} ({self.name})'
