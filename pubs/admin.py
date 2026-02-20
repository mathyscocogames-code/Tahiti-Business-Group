from django.contrib import admin
from django.utils.html import format_html
from .models import Publicite, DemandePublicite


@admin.register(Publicite)
class PubliciteAdmin(admin.ModelAdmin):
    list_display = ['titre', 'emplacement_badge', 'client_nom', 'prix_display', 'actif', 'apercu', 'created_at']
    list_filter = ['emplacement', 'actif']
    list_editable = ['actif']
    search_fields = ['titre', 'client_nom', 'client_email']
    readonly_fields = ['created_at', 'apercu']
    fieldsets = (
        ('Publicité', {'fields': ('titre', 'description', 'image', 'image_url', 'lien', 'emplacement', 'actif')}),
        ('Client', {'fields': ('client_nom', 'client_email', 'client_tel')}),
        ('Facturation', {'fields': ('prix', 'date_debut', 'date_fin')}),
        ('Aperçu', {'fields': ('apercu', 'created_at')}),
    )

    def emplacement_badge(self, obj):
        colors = {'haut': '#ef4444', 'milieu': '#f59e0b', 'bas': '#10b981'}
        labels = {'haut': '🔴 HAUT', 'milieu': '🟡 MILIEU', 'bas': '🟢 BAS'}
        return format_html(
            '<span style="color:{};font-weight:bold">{}</span>',
            colors.get(obj.emplacement, '#fff'),
            labels.get(obj.emplacement, obj.emplacement)
        )
    emplacement_badge.short_description = 'Emplacement'

    def prix_display(self, obj):
        return f"{obj.prix:,} XPF/mois".replace(',', ' ')
    prix_display.short_description = 'Prix'

    def apercu(self, obj):
        img = obj.get_image()
        if img:
            return format_html('<img src="{}" style="max-height:80px;max-width:160px;border-radius:6px">', img)
        return format_html('<span style="color:#6b7280">Aucune image</span>')
    apercu.short_description = 'Aperçu'


@admin.register(DemandePublicite)
class DemandePubliciteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'tel', 'entreprise', 'emplacement_souhaite', 'traite', 'created_at']
    list_filter = ['emplacement_souhaite', 'traite']
    list_editable = ['traite']
    search_fields = ['nom', 'email', 'entreprise']
    readonly_fields = ['created_at']
    actions = ['marquer_traite']

    def marquer_traite(self, request, queryset):
        queryset.update(traite=True)
        self.message_user(request, f"{queryset.count()} demande(s) marquée(s) traitée(s).")
    marquer_traite.short_description = "Marquer comme traitée"