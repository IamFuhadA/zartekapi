from django.db import models
from django.contrib.auth.models import User

class Ride(models.Model):

    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_rider')
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ride {self.id} - {self.rider.username}"
