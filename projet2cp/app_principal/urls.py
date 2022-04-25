

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

    path('switch/<int:switch_id>/portConfig/<int:port_num>',
         views.portConfig, name='portconfig'),

    # va afficher le tableau des vlans
    path('vlan/', views.vlan_tab, name='vlan'),


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
    path('utilisateurs/', views.register_super_user, name='users'),
    path('loginuser', views.connecter, name="login"),

    path('contact/', views.contact, name='contact'),
    path('switch/<int:switch_id>/reformer',views.switch_reforme,name='reformer_switch'),
]
