from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from .models import UserProfile

class Command(BaseCommand):
    help = "Create missing user profiles"

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            UserProfile.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS("User profiles created successfully!"))