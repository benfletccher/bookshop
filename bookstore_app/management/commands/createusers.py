from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from bookstore_app.models import Cadet

class Command(BaseCommand):
    def handle(self, **options):
        groups = ['Cadet', 'Instructor','Admin']
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)