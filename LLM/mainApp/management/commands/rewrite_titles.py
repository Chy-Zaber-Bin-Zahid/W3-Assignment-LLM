from django.core.management.base import BaseCommand
from django.db import transaction
from mainApp.models import Hotel
from mainApp.services.gemini_service import GeminiService
import time


class Command(BaseCommand):
    help = 'Change titles of hotels using Gemini AI'
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
        hotels = Hotel.objects.all()
        total_hotels = hotels.count()
        self.stdout.write(f"{total_hotels} -> hotels found")
        for i in range(0, total_hotels, batch_size):
            batch = hotels[i:i + batch_size]
            self.stdout.write(f"Processing -> {i//batch_size + 1}")
            for hotel in batch:
                try:
                    with transaction.atomic():
                        new_title = gemini_service.rewriteTitle(hotel)
                        if new_title:
                            hotel.property_title = new_title
                            hotel.save()
                            self.stdout.write(
                                self.style.SUCCESS(f"Title change for {hotel.id} to {new_title}")
                            )
                        time.sleep(1)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error at hotel -> {hotel.id}")
                    )