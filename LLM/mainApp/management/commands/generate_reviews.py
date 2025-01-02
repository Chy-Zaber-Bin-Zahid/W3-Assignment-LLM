from django.core.management.base import BaseCommand
from django.db import transaction
from mainApp.models import Hotel, Review
from mainApp.services.gemini_service import GeminiService
import time


class Command(BaseCommand):
    help = 'Reviews make for hotels using Gemini API'
    def addArg(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=2,
            help='Number of hotels to process'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force regenerate reviews even for hotels that already have them'
        )


    def handle(self, *args, **kwargs):
        batch_size = kwargs['batch_size']
        force = kwargs['force']
        gemini_service = GeminiService() 
        if force:
            hotels = Hotel.objects.all()
        else:
            hotels = Hotel.objects.exclude(reviews__isnull=False)
        total_hotels = hotels.count()
        self.stdout.write(f"Found hotels -> {total_hotels}")
        for i in range(0, total_hotels, batch_size):
            batch = hotels[i:i + batch_size]
            self.stdout.write(f"Processing -> {i//batch_size + 1}")
            for hotel in batch:
                try:
                    with transaction.atomic():
                        property_data = {
                            'property_title': hotel.property_title,
                            'city_name': hotel.city_name,
                            'price': f"{hotel.price:.2f}" if hotel.price is not None else "N/A",
                            'rating': f"{hotel.rating:.1f}" if hotel.rating is not None else "3.0"
                        }
                        rating, review = gemini_service.generateReview(property_data)
                        if rating is not None and review:
                            if force:
                                hotel.reviews.all().delete()
                            Review.objects.create(
                                property=hotel,
                                rating=rating,
                                review=review
                            )
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Generated review for: {hotel.property_title}\n"
                                    f"Rating: {rating}\n"
                                    f"Review: {review[:100]}..."
                                )
                            )
                        time.sleep(1)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error found on -> {hotel.id}")
                    )
