from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Publicite, DemandePublicite
from .forms import DemandePubliciteForm


def tarifs_pubs(request):
    pubs_haut = Publicite.objects.filter(emplacement='haut', actif=True).first()
    pubs_milieu = Publicite.objects.filter(emplacement='milieu', actif=True).first()
    pubs_bas = Publicite.objects.filter(emplacement='bas', actif=True).first()

    return render(request, 'pubs/tarifs.html', {
        'pubs_haut': pubs_haut,
        'pubs_milieu': pubs_milieu,
        'pubs_bas': pubs_bas,
        'tarifs': [
            {'emplacement': 'Haut de sidebar', 'prix': 15000, 'desc': 'Meilleure visibilité, premier regard'},
            {'emplacement': 'Milieu de sidebar', 'prix': 10000, 'desc': 'Position centrale, très efficace'},
            {'emplacement': 'Bas de sidebar', 'prix': 5000, 'desc': 'Présence permanente, tarif abordable'},
        ],
    })


def demande_pub(request):
    form = DemandePubliciteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Votre demande a été envoyée ! Nous vous contacterons sous 24h.")
        return redirect('tarifs_pubs')

    return render(request, 'pubs/demande.html', {'form': form})