from django.contrib import admin
from django.utils.html import format_html
from .models import Annonce, Message, Signalement


@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'categorie', 'prix_display', 'statut_badge', 'views', 'boost', 'created_at']
    list_filter = ['statut', 'categorie', 'boost', 'created_at']
    search_fields = ['titre', 'description', 'user__email', 'user__nom']
    list_editable = ['boost']
    actions = ['approuver', 'moderer', 'marquer_vendu']
    readonly_fields = ['views', 'created_at', 'updated_at', 'photos_preview']
    fieldsets = (
        ('Annonce', {'fields': ('titre', 'categorie', 'prix', 'prix_label', 'localisation', 'description')}),
        ('Média', {'fields': ('photos', 'photos_preview')}),
        ('Statut', {'fields': ('statut', 'boost', 'user')}),
        ('Stats', {'fields': ('views', 'created_at', 'updated_at')}),
    )

    def prix_display(self, obj):
        return obj.get_prix_display_label()
    prix_display.short_description = 'Prix'

    def statut_badge(self, obj):
        colors = {'actif': '#00e687', 'modere': '#f59e0b', 'vendu': '#6b7280', 'expire': '#ef4444'}
        color = colors.get(obj.statut, '#6b7280')
        return format_html(
            '<span style="background:{};color:#000;padding:2px 8px;border-radius:4px;font-size:11px">{}</span>',
            color, obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'

    def photos_preview(self, obj):
        if not obj.photos:
            return 'Aucune photo'
        imgs = ''.join(
            f'<img src="{p}" style="height:60px;margin:2px;border-radius:4px">' for p in obj.photos[:4]
        )
        return format_html(imgs)
    photos_preview.short_description = 'Aperçu photos'

    def approuver(self, request, queryset):
        queryset.update(statut='actif')
        self.message_user(request, f"{queryset.count()} annonce(s) approuvée(s).")
    approuver.short_description = "Approuver les annonces sélectionnées"

    def moderer(self, request, queryset):
        queryset.update(statut='modere')
        self.message_user(request, f"{queryset.count()} annonce(s) modérée(s).")
    moderer.short_description = "Modérer les annonces sélectionnées"

    def marquer_vendu(self, request, queryset):
        queryset.update(statut='vendu')
        self.message_user(request, f"{queryset.count()} annonce(s) marquée(s) vendue.")
    marquer_vendu.short_description = "Marquer comme vendu"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['annonce', 'from_user', 'to_user', 'read', 'created_at']
    list_filter = ['read', 'created_at']
    search_fields = ['from_user__email', 'to_user__email', 'content', 'annonce__titre']
    readonly_fields = ['created_at']
    actions = ['marquer_lu']

    def marquer_lu(self, request, queryset):
        queryset.update(read=True)
    marquer_lu.short_description = "Marquer comme lu"

@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display  = ['annonce', 'raison', 'auteur', 'created_at']
    list_filter   = ['raison', 'created_at']
    search_fields = ['annonce__titre', 'details']
    readonly_fields = ['created_at']
    actions = ['supprimer_annonce_signalee']

    def supprimer_annonce_signalee(self, request, queryset):
        for s in queryset:
            s.annonce.statut = 'modere'
            s.annonce.save()
        self.message_user(request, f"{queryset.count()} annonce(s) modérée(s).")
    supprimer_annonce_signalee.short_description = "Modérer l'annonce signalée"
