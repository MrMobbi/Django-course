"""
Django command to wait for the database to be available
"""
from django.core.management.base import BaseCommand

class command(BaseCommand):
    """Django command to wait for Database."""

    def handle(self, *args, **option):
        pass