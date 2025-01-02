from django.core.management.base import BaseCommand
from django.db import transaction
from mainApp.models import Hotel
from mainApp.services.gemini_service import GeminiService
import time


class Command(BaseCommand):
    help = 'Descriptions make for hotels using Gemini API'
    def addArg(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=2,
            help='Number of hotels to process'
        )


    def handle(self, *args, **kwargs):
        batch_size = kwargs['batch_size']
        gemini_service = GeminiService()
        hotels = Hotel.objects.filter(description__isnull=True)
        total_hotels = hotels.count()
        self.stdout.write(f"{total_hotels} -> hotels with no description")
        for i in range(0, total_hotels, batch_size):
            batch = hotels[i:i + batch_size]
            self.stdout.write(f"Processing -> {i//batch_size + 1}")
            for hotel in batch:
                try:
                    with transaction.atomic():
                        property_data = {
                            'property_title': hotel.property_title,
                            'city_name': hotel.city_name,
                            'room_type': hotel.room_type,
                            'price': str(hotel.price),
                            'rating': str(hotel.rating)
                        }
                        description = gemini_service.generateDescription(property_data)
                        if description:
                            hotel.description = description
                            hotel.save()
                            self.stdout.write(
                                self.style.SUCCESS(f"Successfully generated -> {hotel.property_title}")
                            )
                        time.sleep(1)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error on hotel -> {hotel.id}")
                    )