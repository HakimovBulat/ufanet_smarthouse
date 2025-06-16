from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Create admin (superuser) for one time'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='Login').exists():
            User.objects.create_superuser(
                username=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'Login'),
                email=os.environ.get('DJANGO_SUPERUSER_EMAIL', 'login@example.com'),
                password=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Example12345'),
            )
            print("Superuser created.")
        else:
            print("Superuser already exists.")