from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Utilisateur
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import EtudiantRegisterForm, ProfesseurRegisterForm
from .models import Etudiant, Professeur
from .models import Etudiant, Departement, Classe
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Professeur, Cours, Note, Etudiant, EmploiDuTemps


# La vue  page d'accueil 
def home(request):
    return render(request, 'home.html')

# La vue pour la connexion
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.role == 'admin':
                return redirect('dashboard_admin')
            elif user.role == 'professeur':
                return redirect('dashboard_professeur')
            elif user.role == 'etudiant':
                return redirect('dashboard_etudiant')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, "login.html")


# La vue pour le tableau de bord du prof avec tout ses droits
@login_required
def dashboard_professeur(request):
    try:
        professeur = Professeur.objects.get(utilisateur=request.user)
    except Professeur.DoesNotExist:
        return render(request, 'error.html', {'message': 'Accès refusé : vous n\'êtes pas un professeur.'})

    cours_list = Cours.objects.filter(professeur=professeur)
    etudiants = Etudiant.objects.all()  # Ou filtrer par classe/département selon besoin
    notes_list = Note.objects.filter(cours__in=cours_list)
    emplois = EmploiDuTemps.objects.filter(cours__in=cours_list).order_by('jour', 'heure_debut')

    message = ""

    # Ajout / modification d'un cours
    if request.method == "POST":
        if "ajouter_cours" in request.POST:
            nom_cours = request.POST.get("nom_cours")
            if nom_cours:
                Cours.objects.create(nom=nom_cours, professeur=professeur)
                message = "Cours ajouté avec succès."
            else:
                message = "Le nom du cours est requis."

        elif "modifier_cours" in request.POST:
            cours_id = request.POST.get("cours_id")
            nom_cours = request.POST.get("nom_cours")
            if cours_id and nom_cours:
                cours = get_object_or_404(Cours, id=cours_id, professeur=professeur)
                cours.nom = nom_cours
                cours.save()
                message = "Cours modifié avec succès."

        elif "ajouter_note" in request.POST:
            etudiant_id = request.POST.get("etudiant_id")
            cours_id = request.POST.get("cours_id_note")
            session = request.POST.get("session")
            note1 = request.POST.get("note1")
            note2 = request.POST.get("note2")
            note3 = request.POST.get("note3")
            

            if etudiant_id and cours_id and session:
                etudiant = get_object_or_404(Etudiant, id=etudiant_id)
                cours = get_object_or_404(Cours, id=cours_id, professeur=professeur)

                # On essaie de récupérer une note existante pour cet étudiant, ce cours, et cette session
                note_obj, created = Note.objects.get_or_create(
                    etudiant=etudiant,
                    cours=cours,
                    session=session,
                    defaults={'note1': note1 or None, 'note2': note2 or None, 'note3': note3 or None}
                )
                if not created:
                    # Modifier les notes existantes
                    note_obj.note1 = note1 or note_obj.note1
                    note_obj.note2 = note2 or note_obj.note2
                    note_obj.note3 = note3 or note_obj.note3
                    note_obj.save()
                message = "Note enregistrée avec succès."
            else:
                message = "Tous les champs pour la note sont requis."
        elif "ajouter_emploi" in request.POST:
            cours_id = request.POST.get("cours_id_emploi")
            jour = request.POST.get("jour")
            heure_debut = request.POST.get("heure_debut")
            heure_fin = request.POST.get("heure_fin")
        
            if cours_id and jour and heure_debut and heure_fin:
                cours = get_object_or_404(Cours, id=cours_id, professeur=professeur)
                EmploiDuTemps.objects.create(
                    utilisateur=professeur.utilisateur,  # si tu gardes utilisateur dans le modèle
                    cours=cours,
                    jour=jour,
                    heure_debut=heure_debut,
                   heure_fin=heure_fin
                )
        
                message = "Emploi du temps ajouté avec succès."
        
            else:
                message = "Tous les champs de l'emploi du temps sont requis."

        elif "modifier_emploi" in request.POST:
            emploi_id = request.POST.get("emploi_id")
            jour = request.POST.get("jour")
            heure_debut = request.POST.get("heure_debut")
            heure_fin = request.POST.get("heure_fin")

            emploi = get_object_or_404(EmploiDuTemps, id=emploi_id, utilisateur=request.user)
            emploi.jour = jour
            emploi.heure_debut = heure_debut
            emploi.heure_fin = heure_fin
            emploi.save()
            message = "Emploi du temps modifié avec succès."

        elif "supprimer_emploi" in request.POST:
            emploi_id = request.POST.get("emploi_id")
            emploi = get_object_or_404(EmploiDuTemps, id=emploi_id, utilisateur=request.user)
            emploi.delete()
            message = "Emploi du temps supprimé avec succès."

        return redirect('dashboard_professeur')

    context = {
        'professeur': professeur,
        'cours_list': cours_list,
        'etudiants': etudiants,
        'notes_list': notes_list,
        'message': message,
        'session_choices': Note.SESSION_CHOICES,
        'emplois': emplois, # Ajout de l'emploi du temps
      
    }
    return render(request, 'professeur/dashboard_professeur.html', context)
# La vue pour l'inscription d'un etudiant 
def register_etudiant(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        matricule = request.POST['matricule']
        date_naissance = request.POST.get('date_naissance') or None
        adresse = request.POST['adresse']
        email = request.POST.get('email') 
        telephone = request.POST['telephone']
        departement_id = request.POST.get('departement')
        classe_id = request.POST.get('classe')

        # Vérifie si l'utilisateur existe déjà
        if Utilisateur.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
            return redirect('register_etudiant')

        # Création du compte utilisateur
        user = Utilisateur.objects.create_user(username=username, password=password, role='etudiant')
        user.save()

        # Récupération des objets liés
        departement = Departement.objects.get(id=departement_id) if departement_id else None
        classe = Classe.objects.get(id=classe_id) if classe_id else None

        # Création de l'étudiant
        Etudiant.objects.create(
            utilisateur=user,
            nom=nom,
            prenom=prenom,
            email=email,
            matricule=matricule,
            date_naissance=date_naissance,
            adresse=adresse,
            telephone=telephone,
            departement=departement,
            classe=classe
        )

        login(request, user)
        return redirect('dashboard_etudiant')  # Assurez-vous que ce nom de route existe

    # En GET : envoyer les départements et classes pour remplir le formulaire
    departements = Departement.objects.all()
    classes = Classe.objects.all()
   


    return render(request, 'register_etudiant.html', {'departements': departements, 'classes': classes})


# La vue pour l'inscription d'un professeur
def register_professeur(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom') 
        specialite = request.POST.get('specialite')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        date_naissance = request.POST.get('date_naissance')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not all([username, email, nom, prenom, specialite, telephone, date_naissance, password1, password2]):
            messages.error(request, "Tous les champs sont obligatoires.")
            return redirect('register_professeur')

        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('register_professeur')

        if Utilisateur.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return redirect('register_professeur')

        # Création de l'utilisateur avec le rôle 'professeur'
        utilisateur = Utilisateur.objects.create(
            username=username,
            email=email,
            role='professeur',
            password=make_password(password1)  # hash du mot de passe
        )
        utilisateur.save()

        # Création du profil Professeur lié à cet utilisateur
        professeur = Professeur.objects.create(
            utilisateur=utilisateur,
            nom=nom,
            prenom=prenom,
            specialite=specialite,
            telephone=telephone,
            date_naissance=date_naissance
        )
        professeur.save()

        messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
        return redirect('login')

    return render(request, 'register_professeur.html')

# La vue pour le tableau de bord de l'étudiant
@login_required
def dashboard_etudiant(request):
    try:
        etudiant = Etudiant.objects.get(utilisateur=request.user)
    except Etudiant.DoesNotExist:
        return redirect('login')

    notes = Note.objects.filter(etudiant=etudiant).select_related('cours')
    emploi_du_temps = EmploiDuTemps.objects.filter(Professeur=request.user).order_by('jour', 'heure_debut')

    return render(request, 'etudiant/dashboard_etudiant.html', {
        'etudiant': etudiant,
        'notes': notes,
        'emploi_du_temps': emploi_du_temps,
    })

def logout_view(request):
    
    return redirect('home')


from django.contrib.auth.decorators import login_required, user_passes_test



def dashboard_admin(request):
    etudiants = Etudiant.objects.select_related('utilisateur', 'classe').all()
    print(f"Nombre d'étudiants: {etudiants.count()}")
    professeurs = Professeur.objects.select_related('utilisateur').all()
    print(f"Nombre de professeurs: {professeurs.count()}")
    cours = Cours.objects.select_related('professeur__utilisateur').all()
    notes = Note.objects.select_related('etudiant__utilisateur', 'cours').all()
    print(f"Nombre de notes: {notes.count()}")

    context = {
        'etudiants': etudiants,
        'professeurs': professeurs,
        'cours': cours,
        'notes': notes,
    }
    return render(request, 'admin/dashboard.html', context)
