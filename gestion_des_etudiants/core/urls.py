from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     
    
    path('register/etudiant/', views.register_etudiant, name='register_etudiant'),
    path('dashboard/etudiant/', views.dashboard_etudiant, name='dashboard_etudiant'),

    

    path('register/professeur/', views.register_professeur, name='register_professeur'),
    path('dashboard/professeur/', views.dashboard_professeur, name='dashboard_professeur'),
 

    # Tableau de bord
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),


]


