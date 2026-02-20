from django.db import models
from django.conf import settings

STATUT_CHOICES = [
    ('en_attente', 'En attente'),
    ('valide', 'Validé'),
    ('refuse', 'Refusé'),
]


class ArticlePromo(models.Model):
    pro_user   = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='promos'
    )
    titre      = models.CharField(max_length=200)
    contenu    = models.TextField()
    lien_promo = models.URLField(blank=True)
    statut     = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Promo'
        verbose_name_plural = 'Promos'

    def __str__(self):
        return self.titre


class ArticleInfo(models.Model):
    auteur       = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='infos'
    )
    titre        = models.CharField(max_length=200)
    contenu      = models.TextField()
    source_media = models.URLField(blank=True, help_text="Lien vers l'article source")
    statut       = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Info'
        verbose_name_plural = 'Infos'

    def __str__(self):
        return self.titre


class ArticleNouveaute(models.Model):
    pro_user         = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='nouveautes'
    )
    titre            = models.CharField(max_length=200)
    contenu          = models.TextField()
    lien_redirection = models.URLField(blank=True)
    statut           = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Nouveauté'
        verbose_name_plural = 'Nouveautés'

    def __str__(self):
        return self.titre