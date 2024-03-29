from django.urls import path
from .import views

app_name = "app_principal"


urlpatterns = [
    # SWITCHS
    # va afficher le tableau des switchs
    path('switch/', views.switchtab, name='switch'),
    path('switch/ajout', views.ajoutswitch, name='add_switch'),
    path('switch/plus_info/<int:switch_id>',
         views.plus_info_switch, name='plus_info_switch'),
    path('switch/<int:switch_id>/portConfig/<int:port_num>',
         views.portConfig, name='portconfig'),
    path('switch/<int:switch_id>/configurer',
         views.switchConfig, name='config_switch'),
    path('switch/recherche_element_suiv', views.recherche_elem_suiv, name='ele_suiv'),

    # VLANS
    path('vlan/', views.vlan_tab, name='vlan'),
    path('vlan/ajout', views.ajoutvlan, name='add_vlan'),
    path('vlan/mise_à_jour/<int:id>', views.updateVlan),
    path('vlan/supprimer/<int:id>', views.deleteVlan),

    # PORTS
    # va afficher le tableau des ports
    path('switch/<int:switch_id>/port_tab/', views.port_tab, name='port'),

    # MODELE_SWITCH
    path('Modele/', views.modele_tab, name='modele'),
    path('Modele/ajout', views.ajout_modele, name='ajout_modele'),

    # ACCUEIL
    path('', views.PageAccueil, name='home'),
     path('nos_Serivces', views.servicepage, name='service'),
   



    # AUTHENTIFICATION
    path('Deconnecter', views.logout_user, name='logout'),
    path('Se Connecter', views.connecter, name="login"),
    path('changer_mot_passe/', views.password_change, name='password_change'),
    path('Recuperer_mot_passe/', views.PasswordReset.as_view(), name='password_reset'),
    path('mot_de_passe_recuperée/', views.PasswordResetDone.as_view(),
         name='password_reset_done'),
    path('reset-password/<uidb64>/<token>/',
         views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset-password-complete/', views.PasswordResetComplete.as_view(),
         name='password_reset_complete'),


    # CONTACT
    path('contact/', views.contact, name='contact'),


    # GESTION DES UTILISATEURS
    path('utilisateurs/', views.gestion_user, name='users'),
    path('utilisateurs/ajouter_super_utilisateur',
         views.register_super_user, name='create_superuser'),
    path('utilisateurs/ajouter_utilisateur',
         views.register_user, name='ajouter-user'),
    path('utilisateurs/corbeille', views.corbeille, name='corbeille'),
    path('utilisateurs/activer_utilisateur/<int:user_id>',
         views.activer_user, name='activer_user'),
    path('utilisateurs/modifier_permissions/<int:user_id>',
         views.modif_permissions_user, name='modif_permissions_user'),

    # STATISTIQUES ET HISTORIQUE
    path('statistiques/', views.statistique, name='statistique'),
    path('historique/', views.plus_historique, name='historique'),
    
    
    # PROFIL
     path('Mon-Compte', views.p, name='c'),
     path('Mon-Compte/Modifier', views.profilUpdate, name='ch'),
     #path('Changer_mot_de_passe', views.motpass, name='cha'),

      #Help page
    path('aide',views.help, name='aide'),
    path('compte',views.compte),
    path('vlan_aide',views.vln),
    path('port_aide',views.port),
    path('switch_aide',views.swt),
    path('statistique',views.stat),
    path('FAQ',views.faq),

     path('accueil', views.accueil1, name='accueil1'),

]
