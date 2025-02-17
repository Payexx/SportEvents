from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Profil {self.user.username}"

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('bieg', 'Bieg'),
        ('rower', 'Rower'),
        ('nordic_walking', 'Nordic Walking'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    max_participants = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='bieg')

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"

    def available_spots(self):
        return self.max_participants - self.registrations.count()

class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"