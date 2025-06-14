from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Etudiant, Professeur, Cours, Note, EmploiDuTemps, Departement, Classe

# Admin pour le modèle Utilisateur personnalisé
class UtilisateurAdmin(UserAdmin):
    fieldsets = tuple(list(UserAdmin.fieldsets) + [
        ('Rôle', {'fields': ('role',)}),
    ])
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Etudiant)
admin.site.register(Professeur)
admin.site.register(Cours)
admin.site.register(Note)
admin.site.register(EmploiDuTemps)
admin.site.register(Departement)
admin.site.register(Classe)
