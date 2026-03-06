from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('mon-compte/', views.mon_compte, name='mon_compte'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('moderer/<int:pk>/', views.moderer_annonce, name='moderer_annonce'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('supprimer-compte/', views.supprimer_compte, name='supprimer_compte'),
]