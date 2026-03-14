"""
Commande de gestion pour expirer les publicités dont la date de fin est dépassée
et nettoyer les paiements en attente depuis plus de 24h.

Usage : python manage.py expire_pubs
Recommandé : exécuter quotidiennement via cron ou Railway scheduled task.
"""
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from pubs.models import Publicite


class Command(BaseCommand):
    help = 'Expire les pubs payées dont la date de fin est dépassée et nettoie les paiements en attente.'

    def handle(self, *args, **options):
        today = date.today()

        # 1. Expirer les pubs actives dont la date_fin est dépassée
        expired = Publicite.objects.filter(
            actif=True,
            payment_status='paid',
            date_fin__lt=today,
        ).update(actif=False, payment_status='expired')

        if expired:
            self.stdout.write(self.style.WARNING(f'{expired} pub(s) expirée(s).'))

        # 2. Nettoyer les paiements en attente > 24h (jamais finalisés)
        cutoff = timezone.now() - timedelta(hours=24)
        stale = Publicite.objects.filter(
            payment_status='pending',
            created_at__lt=cutoff,
        ).update(payment_status='failed')

        if stale:
            self.stdout.write(self.style.WARNING(f'{stale} paiement(s) en attente nettoyé(s).'))

        if not expired and not stale:
            self.stdout.write(self.style.SUCCESS('Rien à faire.'))
