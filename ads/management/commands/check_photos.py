"""Liste les annonces dont les photos pointent vers /media/ (perdues)."""
from django.core.management.base import BaseCommand
from ads.models import Annonce


class Command(BaseCommand):
    help = "Liste les annonces avec des photos locales (/media/) perdues"

    def handle(self, *args, **options):
        broken = []
        for a in Annonce.objects.exclude(photos=[]):
            local = [p for p in a.photos if p.startswith('/media/')]
            if local:
                broken.append((a, local))

        if not broken:
            self.stdout.write(self.style.SUCCESS(
                "Aucune annonce avec des photos locales perdues."
            ))
            return

        self.stdout.write(self.style.WARNING(
            f"{len(broken)} annonce(s) avec photos locales perdues :\n"
        ))
        for a, photos in broken:
            user = a.user
            self.stdout.write(
                f"  - [{a.pk}] {a.titre}\n"
                f"    Utilisateur : {user.nom or 'N/A'} ({user.email})\n"
                f"    Photos perdues : {len(photos)}/{len(a.photos)}\n"
            )
