from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='userprofiles/', blank=True, null=True)

    def __str__(self):
        return self.full_name
    

class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class RSVP(models.Model):
    STATUS_GOING = 'Going'
    STATUS_MAYBE = 'Maybe'
    STATUS_NOT_GOING = 'Not Going'

    STATUS_CHOICES = [
    (STATUS_GOING, 'Going'),
    (STATUS_MAYBE, 'Maybe'),
    (STATUS_NOT_GOING, 'Not Going'),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"
    
class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField()

    def __str__(self):
        return f"{self.event.title} - {self.rating}/5"

