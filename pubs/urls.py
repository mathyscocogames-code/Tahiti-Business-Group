from django.urls import path
from . import views

urlpatterns = [
    path('tarifs/', views.tarifs_pubs, name='tarifs_pubs'),
    path('demande/', views.demande_pub, name='demande_pub'),
]