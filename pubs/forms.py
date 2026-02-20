from django import forms
from .models import DemandePublicite


class DemandePubliciteForm(forms.ModelForm):
    class Meta:
        model = DemandePublicite
        fields = ['nom', 'email', 'tel', 'entreprise', 'emplacement_souhaite', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'votre@email.com'}),
            'tel': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '89 XX XX XX'}),
            'entreprise': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nom de votre entreprise'}),
            'emplacement_souhaite': forms.Select(attrs={'class': 'form-input'}),
            'message': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 4,
                'placeholder': 'Décrivez votre besoin...'
            }),
        }