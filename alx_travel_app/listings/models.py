from django.db import models
import uuid
from django.db.models import TextChoices
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Listings(models.Model):
    listing_id = models.CharField(
        primary_key=True,
        max_length=36,
        default=str(uuid.uuid4()),
        editable=False
    )
    name = models.CharField(max_length=63, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    Location = models.CharField(max_length=255, null=False, blank=False)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BookingStatus(TextChoices):
    PENDING = 'PENDING', 'Pending'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    CANCELLED = 'CANCELLED', 'Cancelled'

class Booking(models.Model):
    booking_id = models.CharField(
        primary_key=True,
        max_length=36,
        default=str(uuid.uuid4()),
        editable=False
    )
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')

    status = models.CharField(
        max_length=10,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )
    check_in = models.DateField(null=False, blank=False, auto_now_add=True)
    check_out = models.DateField(null=False, blank=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.listing.name} - {self.guest.username}'


class Review(models.Model):
    review_id = models.CharField(
        primary_key=True,
        max_length=36,
        default=str(uuid.uuid4()),
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(null=False,
                                 blank=False,
                                 validators=[MinValueValidator(1), MaxValueValidator(5)],
                                 help_text='Rating must be between 1 and 5'
                                )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.listing.name} - {self.user.username} - {self.rating}'
