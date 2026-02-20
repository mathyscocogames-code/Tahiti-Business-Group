from django.contrib import admin
from .models import ArticlePromo, ArticleInfo, ArticleNouveaute


@admin.register(ArticlePromo)
class ArticlePromoAdmin(admin.ModelAdmin):
    list_display = ['titre', 'pro_user', 'statut', 'created_at']
    list_filter = ['statut']
    list_editable = ['statut']
    search_fields = ['titre', 'contenu']


@admin.register(ArticleInfo)
class ArticleInfoAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'statut', 'created_at']
    list_filter = ['statut']
    list_editable = ['statut']
    search_fields = ['titre', 'contenu']


@admin.register(ArticleNouveaute)
class ArticleNouveauteAdmin(admin.ModelAdmin):
    list_display = ['titre', 'pro_user', 'statut', 'created_at']
    list_filter = ['statut']
    list_editable = ['statut']
    search_fields = ['titre', 'contenu']