"""Jour 5 — Fixes : dropdown hover + billboard milieu + tarifs + rename"""
import re, os

# ── 1. pubs/models.py — nouveau billboard_milieu + nouveaux tarifs ────────────
pubs_model = """\
from django.db import models

EMPLACEMENTS = [
    ('billboard',        'Billboard Haut (25\u202f000 XPF/mois)'),
    ('billboard_milieu', 'Billboard Milieu (15\u202f000 XPF/mois)'),
    ('haut',             'Sidebar Haut (10\u202f000 XPF/mois)'),
    ('milieu',           'Sidebar Milieu (7\u202f000 XPF/mois)'),
    ('bas',              'Sidebar Bas (5\u202f000 XPF/mois)'),
]

PRIX_PAR_EMPLACEMENT = {
    'billboard':        25000,
    'billboard_milieu': 15000,
    'haut':             10000,
    'milieu':            7000,
    'bas':               5000,
}


class Publicite(models.Model):
    titre        = models.CharField(max_length=200)
    description  = models.CharField(max_length=300, blank=True)
    image        = models.ImageField(upload_to='pubs/', blank=True, null=True)
    image_url    = models.URLField(blank=True, help_text="URL externe si pas d'upload")
    lien         = models.URLField(blank=True)
    emplacement  = models.CharField(max_length=20, choices=EMPLACEMENTS)
    prix         = models.IntegerField(default=0)
    actif        = models.BooleanField(default=True)
    client_nom   = models.CharField(max_length=150, blank=True)
    client_email = models.EmailField(blank=True)
    client_tel   = models.CharField(max_length=20, blank=True)
    date_debut   = models.DateField(null=True, blank=True)
    date_fin     = models.DateField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Publicit\u00e9'
        verbose_name_plural = 'Publicit\u00e9s'
        ordering = ['emplacement', '-actif']

    def __str__(self):
        return f"{self.titre} ({self.get_emplacement_display()})"

    def save(self, *args, **kwargs):
        if not self.prix:
            self.prix = PRIX_PAR_EMPLACEMENT.get(self.emplacement, 0)
        super().save(*args, **kwargs)

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or None


class DemandePublicite(models.Model):
    nom                  = models.CharField(max_length=150)
    email                = models.EmailField()
    tel                  = models.CharField(max_length=20, blank=True)
    entreprise           = models.CharField(max_length=200, blank=True)
    emplacement_souhaite = models.CharField(max_length=20, choices=EMPLACEMENTS)
    message              = models.TextField(blank=True)
    traite               = models.BooleanField(default=False)
    created_at           = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Demande de pub'
        verbose_name_plural = 'Demandes de pub'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nom} \u2014 {self.emplacement_souhaite}"
"""
with open('pubs/models.py', 'w', encoding='utf-8') as f:
    f.write(pubs_model)
print('pubs/models.py OK')

# ── 2. pubs/context_processors.py — ajouter pub_billboard_milieu ─────────────
ctx = """\
from .models import Publicite
from ads.models import SOUS_CATEGORIES


def sidebar_pubs(request):
    return {
        'pub_billboard':        Publicite.objects.filter(emplacement='billboard',        actif=True).first(),
        'pub_billboard_milieu': Publicite.objects.filter(emplacement='billboard_milieu', actif=True).first(),
        'pub_haut':             Publicite.objects.filter(emplacement='haut',             actif=True).first(),
        'pub_milieu':           Publicite.objects.filter(emplacement='milieu',           actif=True).first(),
        'pub_bas':              Publicite.objects.filter(emplacement='bas',              actif=True).first(),
        'sous_categories':      SOUS_CATEGORIES,
    }
"""
with open('pubs/context_processors.py', 'w', encoding='utf-8') as f:
    f.write(ctx)
print('context_processors.py OK')

# ── 3. ads/models.py — renommer vehicules-4x4 ────────────────────────────────
with open('ads/models.py', encoding='utf-8') as f:
    ads_m = f.read()
ads_m = ads_m.replace(
    "('vehicules-4x4',         '4x4 & SUV (Tahiti)')",
    "('vehicules-4x4',         'Voitures / 4 roues')"
)
with open('ads/models.py', 'w', encoding='utf-8') as f:
    f.write(ads_m)
print('ads/models.py rename OK')

# ── 4. _sidebar_pubs.html — mettre à jour prix affiché ───────────────────────
with open('templates/partials/_sidebar_pubs.html', encoding='utf-8') as f:
    sidebar = f.read()
sidebar = sidebar.replace('15 000 XPF</div>\n        <div class="pub-empty__sub">Emplacement premium',
                          '10\u202f000 XPF</div>\n        <div class="pub-empty__sub">Emplacement premium')
sidebar = sidebar.replace('10 000 XPF</div>\n        <div class="pub-empty__sub">Position centrale',
                          '7\u202f000 XPF</div>\n        <div class="pub-empty__sub">Position centrale')
with open('templates/partials/_sidebar_pubs.html', 'w', encoding='utf-8') as f:
    f.write(sidebar)
print('_sidebar_pubs.html OK')

# ── 5. base.html — renommer dropdown + mettre à jour footer tarifs ─────────────
with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

# Rename in dropdown
base = base.replace(
    '>4x4 &amp; SUV (Tahiti)<',
    '>Voitures / 4 roues<'
)

# Footer prices: add billboard milieu, update sidebar prices
base = base.replace(
    '            <div class="text-xs">Billboard \u2014 <strong class="text-gray-800">25\u202f000 XPF/mois</strong></div>\n'
    '            <div class="text-xs">Sidebar Haut \u2014 <strong class="text-gray-800">15\u202f000 XPF/mois</strong></div>\n'
    '            <div class="text-xs">Sidebar Milieu \u2014 <strong class="text-gray-800">10\u202f000 XPF/mois</strong></div>\n'
    '            <div class="text-xs">Sidebar Bas \u2014 <strong class="text-gray-800">5\u202f000 XPF/mois</strong></div>',
    '            <div class="text-xs">Billboard Haut \u2014 <strong class="text-gray-800">25\u202f000 XPF/mois</strong></div>\n'
    '            <div class="text-xs">Billboard Milieu \u2014 <strong class="text-gray-800">15\u202f000 XPF/mois</strong></div>\n'
    '            <div class="text-xs">Sidebar Haut \u2014 <strong class="text-gray-800">10\u202f000 XPF/mois</strong></div>\n'
    '            <div class="text-xs">Sidebar Milieu \u2014 <strong class="text-gray-800">7\u202f000 XPF/mois</strong></div>\n'
    '            <div class="text-xs">Sidebar Bas \u2014 <strong class="text-gray-800">5\u202f000 XPF/mois</strong></div>'
)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('base.html OK')

print('\nAll patches applied!')