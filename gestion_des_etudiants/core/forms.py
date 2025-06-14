from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class EtudiantRegisterForm(UserCreationForm):
    nom = forms.CharField(max_length=100)
    prenom = forms.CharField(max_length=100)
    matricule = forms.CharField(max_length=20)
    date_naissance = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    adresse = forms.CharField(max_length=255)
    telephone = forms.CharField(max_length=20)
    departement = forms.ModelChoiceField(queryset=None)
    classe = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Utilisateur
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(EtudiantRegisterForm, self).__init__(*args, **kwargs)
        from .models import Departement, Classe
        self.fields['departement'].queryset = Departement.objects.all()
        self.fields['classe'].queryset = Classe.objects.all()


class ProfesseurRegisterForm(UserCreationForm):
    nom = forms.CharField(max_length=100)
    prenom = forms.CharField(max_length=100)
    email = forms.EmailField()
    date_naissance = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    specialite = forms.CharField(max_length=100)
    telephone = forms.CharField(max_length=20)

    class Meta:
        model = Utilisateur
        fields = ['username', 'password1', 'password2']


