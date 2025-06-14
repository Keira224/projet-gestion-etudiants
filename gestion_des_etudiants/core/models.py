from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Modèle utilisateur personnalisé
class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('etudiant', 'Étudiant'),
        ('professeur', 'Professeur'),
        ('admin', 'Administrateur'),
        ('cadre', 'Cadre'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


# Modèle Département
class Departement(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom


# Modèle Classe
class Classe(models.Model):
    CLASSE_CHOICES = [
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
    ]
    nom = models.CharField(max_length=2, choices=CLASSE_CHOICES, unique=True)

    def __str__(self):
        return self.get_nom_display()


# Modèle Étudiant
class Etudiant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    matricule = models.CharField(max_length=20)
    date_naissance = models.DateField(null=True, blank=True)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True)
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.matricule}"


# Modèle Professeur
class Professeur(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    date_naissance = models.DateField(default=datetime.date(1990, 1, 1), null=True, blank=True)
    specialite = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.utilisateur.get_full_name()}"


# Modèle Cours
class Cours(models.Model):
    nom = models.CharField(max_length=100)
    professeur = models.ForeignKey(Professeur, on_delete=models.SET_NULL, null=True, blank=True, related_name='cours')

    def __str__(self):
        return self.nom


# Modèle Note
class Note(models.Model):
    SESSION_CHOICES = (
        ('session1', 'Session 1'),
        ('session2', 'Session 2'),
    )
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    note1 = models.FloatField(null=True, blank=True)
    note2 = models.FloatField(null=True, blank=True)
    note3 = models.FloatField(null=True, blank=True)
    session = models.CharField(max_length=10, choices=SESSION_CHOICES, default='session1')

    def __str__(self):
        return f"{self.etudiant.utilisateur.username} - {self.cours.nom} ({self.session}) : {self.note1}, {self.note2}, {self.note3}"


# Modèle Emploi du temps
class EmploiDuTemps(models.Model):
    Professeur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    jour = models.CharField(max_length=10)
    heure_debut = models.TimeField(null=True, blank=True)
    heure_fin = models.TimeField(null=True, blank=True)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Professeur.username} - {self.jour} ({self.heure_debut}-{self.heure_fin})"
