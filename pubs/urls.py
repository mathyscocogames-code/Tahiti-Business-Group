from django.urls import path
from . import views

urlpatterns = [
    path('tarifs/',              views.tarifs_pubs,        name='tarifs_pubs'),
    path('demande/',             views.demande_pub,        name='demande_pub'),
    path('creer/',               views.pub_creer,          name='pub_creer'),
    path('<int:pk>/modifier/',   views.pub_modifier,       name='pub_modifier'),
    path('<int:pk>/supprimer/',  views.pub_supprimer,      name='pub_supprimer'),
    path('<int:pk>/toggle/',     views.pub_toggle,         name='pub_toggle'),
    # Self-service : déposer + payer
    path('deposer/',             views.deposer_pub,        name='deposer_pub'),
    path('paiement/<int:pk>/',   views.initier_paiement,   name='initier_paiement'),
    path('paiement/retour/',     views.retour_paiement,    name='retour_paiement'),
    path('paiement/ipn/',        views.ipn_paiement,       name='ipn_paiement'),
]
