from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "Cree le compte admin si absent"

    def handle(self, *args, **options):
        email = "admin@tahitibusinessgroup.com"
        if User.objects.filter(email=email).exists():
            self.stdout.write(f"Admin {email} existe deja.")
            return
        User.objects.create_superuser(
            email=email,
            password="TBG-Admin-2026!Secure",
            nom="Admin TBG",
        )
        self.stdout.write(self.style.SUCCESS(f"Admin {email} cree avec succes."))
