

from django.urls import path
from .import views
app_name = "app_principal"

urlpatterns = [
    # va afficher le tableau des switchs
    path('switch/', views.switchtab, name='switch'),
    path('switch/ajout', views.ajoutswitch, name='add_switch'),
    path('vlan/ajout', views.ajoutvlan, name='add'),

    path('switch/<int:switch_id>/configurer',
         views.switchConfig, name='config_switch'),
    path('switch/plus_info/<int:switch_id>', views.plus_info_switch, name='plus_info_switch'),
    path('switch/<int:switch_id>/portConfig/<int:port_num>',
         views.portConfig, name='portconfig'),

    # va afficher le tableau des vlans
    path('vlan/', views.vlan_tab, name='vlan'),


<<<<<<< HEAD
from  django.urls import path, reverse
from  .import views

app_name="app_principal"

urlpatterns = [ 
     path('switch/',views.switchtab,name='switch'), #va afficher le tableau des switchs
     path('switch/ajout',views.ajoutswitch,name='add_switch'),
     path('vlan/ajout',views.ajoutvlan,name='add_vlan'),

     path('switch/<int:switch_id>/configurer',views.switchConfig,name='config_switch'),


     path('vlan/',views.vlan_tab,name='vlan'), #va afficher le tableau des vlans


     path('port/',views.port_tab,name='port'), #va afficher le tableau des ports
     path('logout', views.logout_user, name='logout'),
 
     path('switch/<int:switch_id>/configurer',views.switchConfig,name='add'),
     path('home',views.acul,name='home'),
     path('Notre_serivce',views.servicepage,name='service'),
     path('register/',views.register,name='register'),
    # path('login/',views.login,name='register'),
     path('user/',views.profil,name='add'),
     path('user_form/',views.formprofil,name='user_form'),
    
  #Modeles
     path('modele/',views.modele_tab,name='modele'), #va afficher le tableau des modeles

  #eset password

     path('utilisateurs/',views.register_super_user,name='users'),
     path('login', views.connecter, name="login"),
  
    # path("password_reset", views.password_reset_request, name="password_reset") ,
     
     path('change-password/', views.password_change , name ='password_change'),
     path('reset-password/', views.PasswordReset.as_view(),name ='password_reset'),
     path('reset-password-done/', views.PasswordResetDone.as_view(),name ='password_reset_done'),
     path('reset-password/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(),name ='password_reset_confirm'),
     path('reset-password-complete/', views.PasswordResetComplete.as_view(),name ='password_reset_complete'),
=======
    # va afficher le tableau des ports
    path('switch/<int:switch_id>/port_tab/', views.port_tab, name='port'),
    path('logout', views.logout_user, name='logout'),

    path('switch/<int:switch_id>/configurer', views.switchConfig, name='add'),
    path('home', views.acul, name='home'),
    path('Notre_serivce', views.servicepage, name='service'),
    path('register/', views.register, name='register'),
    # path('login/',views.login,name='register'),
    path('user/', views.profil, name='add'),
    path('user_form/', views.formprofil, name='add'),

    # Modeles
    # va afficher le tableau des modeles
    path('modele/', views.modele_tab, name='modele'),
    path('modele/ajout', views.ajout_modele, name='ajout_modele'),
    # gestion_user
    path('loginuser', views.connecter, name="login"),

    path('contact/', views.contact, name='contact'),
    path('switch/<int:switch_id>/reformer',views.switch_reforme,name='reformer_switch'),
  #gestion_user
  path('utilisateurs/',views.gestion_user,name='users'),
  path('utilisateurs/ajouter_super_utilisateur',views.register_super_user,name='create_superuser'),
  path('utilisateurs/ajouter_utilisateur',views.register_user,name='ajouter-user'),
  path('utilisateurs/corbeille',views.corbeille,name='corbeille'),
  path('utilisateurs/activer_utilisateur/<int:user_id>',views.activer_user,name='activer_user'),
  path('utilisateurs/modifier_permissions/<int:user_id>',views.modif_permissions_user,name='modif_permissions_user'),
>>>>>>> 0e3c1f41c8fdda7f963135c911a238f88c58681a

]
