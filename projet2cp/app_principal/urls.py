from django.urls import path
from .import views

app_name = "app_principal"


urlpatterns = [
    #SWITCHS
     path('switch/',views.switchtab,name='switch'), #va afficher le tableau des switchs
     path('switch/ajout',views.ajoutswitch,name='add_switch'),
     path('switch/plus_info/<int:switch_id>', views.plus_info_switch, name='plus_info_switch'),
     path('switch/<int:switch_id>/portConfig/<int:port_num>',views.portConfig, name='portconfig'),    
     path('switch/<int:switch_id>/configurer',views.switchConfig,name='config_switch'),
     path('switch/<int:switch_id>/defectueux',views.switch_defectueux,name='defect_switch'),

    
    #VLANS
     path('vlan/', views.vlan_tab, name='vlan'),
     path('vlan/ajout', views.ajoutvlan, name='add_vlan'),
     path('vlan/edit/<int:id>',views.updateVlan),
     path('vlan/delete/<int:id>',views.deleteVlan),

     #PORTS
     path('port/',views.port_tab,name='port'), #va afficher le tableau des ports
     path('switch/<int:switch_id>/port_tab/', views.port_tab, name='port'),

     #MODELE_SWITCH
     path('modele/', views.modele_tab, name='modele'),
     path('modele/ajout', views.ajout_modele, name='ajout_modele'),
     
     #ACCUEIL
     path('home',views.acul,name='home'),
     path('Notre_serivce',views.servicepage,name='service'),
  
    
    
    # AUTHENTIFICATION
        # path('login/',views.login,name='register'),
        # path("password_reset", views.password_reset_request, name="password_reset") ,
     path('logout', views.logout_user, name='logout'),
     path('loginuser', views.connecter, name="login"),
     #path('register/', views.register, name='register'),
     path('change-password/', views.password_change , name ='password_change'),
     path('reset-password/', views.PasswordReset.as_view(),name ='password_reset'),
     path('reset-password-done/', views.PasswordResetDone.as_view(),name ='password_reset_done'),
     path('reset-password/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(),name ='password_reset_confirm'),
     path('reset-password-complete/', views.PasswordResetComplete.as_view(),name ='password_reset_complete'),
    

     #PROFIL
     path('profile/',views.profil,name='profile'),
     path('user_form/',views.formprofil,name='user_form'),


     #CONTACT
     path('contact/', views.contact, name='contact'),
  
  
     #GESTION DES UTILISATEURS
     path('utilisateurs/',views.gestion_user,name='users'),
     path('utilisateurs/ajouter_super_utilisateur',views.register_super_user,name='create_superuser'),
     path('utilisateurs/ajouter_utilisateur',views.register_user,name='ajouter-user'),
     path('utilisateurs/corbeille',views.corbeille,name='corbeille'),
     path('utilisateurs/activer_utilisateur/<int:user_id>',views.activer_user,name='activer_user'),
     path('utilisateurs/modifier_permissions/<int:user_id>',views.modif_permissions_user,name='modif_permissions_user'),
 
    #STATISTIQUES
    path('statistique/',views.statistique, name='statistique'),
]
