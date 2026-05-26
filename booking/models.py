from django.db import models
from django.conf import settings
from rooms.models import Room

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    check_in = models.DateField()
    check_out = models.DateField()

    guests = models.IntegerField(default=1)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    special_requests = models.TextField(blank=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, default='pending')
    payment_status = models.CharField(max_length=20, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.room.name}"