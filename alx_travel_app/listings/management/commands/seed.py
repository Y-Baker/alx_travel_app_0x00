from django.core.management.base import BaseCommand
from listings.models import Listings, Booking, Review
from django.contrib.auth.models import User
from faker import Faker
import random
from datetime import datetime, timedelta



from django.core.management.base import BaseCommand
from listings.models import Listings, Booking, Review, BookingStatus
from django.contrib.auth.models import User
from faker import Faker
import random
from datetime import timedelta
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Seed the database with sample data for Listings, Bookings, and Reviews'

    def handle(self, *args, **kwargs):
        fake = Faker()

        Listings.objects.all().delete()
        Booking.objects.all().delete()
        Review.objects.all().delete()
        User.objects.filter(is_staff=False).delete()

        self.stdout.write('Creating users...')
        users = [
            User.objects.create_user(username=fake.user_name(), email=fake.email(), password='password')
            for _ in range(10)
        ]

        self.stdout.write('Creating listings...')
        listings = [
            Listings.objects.create(
                name=fake.company(),
                description=fake.text(max_nb_chars=200),
                Location=fake.city(),
                price_per_night=round(random.uniform(50.0, 500.0), 2),
                host=random.choice(users),
                created_at=now(),
                updated_at=now()
            )
            for _ in range(15)
        ]

        self.stdout.write('Creating bookings...')
        for listing in listings:
            for _ in range(random.randint(1, 5)):  # 1 to 5 bookings per listing
                guest = random.choice(users)
                check_in = fake.date_this_year(before_today=False, after_today=True)
                check_out = check_in + timedelta(days=random.randint(1, 7))
                total_price = (check_out - check_in).days * listing.price_per_night

                Booking.objects.create(
                    listing=listing,
                    guest=guest,
                    status=random.choice([BookingStatus.PENDING, BookingStatus.CONFIRMED, BookingStatus.CANCELLED]),
                    check_in=check_in,
                    check_out=check_out,
                    total_price=round(total_price, 2),
                    created_at=now(),
                    updated_at=now()
                )

        self.stdout.write('Creating reviews...')
        for listing in listings:
            for _ in range(random.randint(1, 3)):
                user = random.choice(users)
                Review.objects.create(
                    user=user,
                    listing=listing,
                    rating=random.randint(1, 5),
                    comment=fake.sentence(),
                    created_at=now(),
                    updated_at=now()
                )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
