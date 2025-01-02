from django.core.management.base import BaseCommand
from django.db import transaction
from mainApp.models import Hotel, Summary
from mainApp.services.gemini_service import GeminiService
import time


class Command(BaseCommand):
    help = 'Make summary for hotels using Gemini API'
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
        hotels = Hotel.objects.filter(description__isnull=False).exclude(summaries__isnull=False)
        total_hotels = hotels.count()
        self.stdout.write(f"{total_hotels} -> hotels with no summaries")
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
                            'rating': f"{hotel.rating:.1f}" if hotel.rating is not None else "N/A",
                            'description': hotel.description or "Not available"
                        }
                        summary = gemini_service.generateSummary(property_data)
                        if summary:
                            Summary.objects.create(
                                property=hotel,
                                summary=summary
                            )
                            self.stdout.write(
                                self.style.SUCCESS(f"Summary made on -> {hotel.property_title}")
                            )
                        time.sleep(1)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error found on -> {hotel.id}")
                    )
