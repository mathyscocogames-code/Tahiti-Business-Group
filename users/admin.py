from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from .models import User


def _export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="utilisateurs.csv"'
    writer = csv.writer(response)
    writer.writerow(['email', 'nom', 'role', 'tel', 'date_joined', 'is_active'])
    for u in queryset:
        writer.writerow([u.email, u.nom, u.role, u.tel, u.date_joined, u.is_active])
    return response
_export_csv.short_description = "Exporter en CSV"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'nom', 'role_badge', 'tel', 'abonnement_promo_actif', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['email', 'nom', 'tel']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined']
    actions = [_export_csv]

    fieldsets = (
        ('Identifiants', {'fields': ('email', 'password')}),
        ('Infos personnelles', {'fields': ('nom', 'tel', 'avatar')}),
        ('Compte Pro', {'fields': ('nom_entreprise', 'numero_tahiti', 'abonnement_promo_actif')}),
        ('Rôle & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'role', 'password1', 'password2'),
        }),
    )

    def role_badge(self, obj):
        colors = {'admin': '#ef4444', 'pro': '#1a6cf1', 'personnel': '#00e687'}
        color = colors.get(obj.role, '#6b7280')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:4px;font-size:11px">{}</span>',
            color, obj.get_role_display()
        )
    role_badge.short_description = 'Rôle'