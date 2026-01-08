from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        email = config('DJANGO_SUPERUSER_EMAIL', default='admin@atena.com')
        password = config('DJANGO_SUPERUSER_PASSWORD', default='admin')
        
        if not User.objects.filter(email=email).exists():
            self.stdout.write(f'Creating superuser {email}...')
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
