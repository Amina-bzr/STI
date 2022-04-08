from django.urls import path
#from .views import viewName

from .import views


app_name="app_principal"

urlpatterns = [
  path('switch/',views.switchtab,name='switch'), #va afficher le tableau des switchs
  path('switch/ajout',views.ajoutswitch,name='add_switch'),
  path('vlan/ajout',views.ajoutvlan,name='add'),
  path('switch/<int:switch_id>/configurer',views.switchConfig,name='config_switch'),

  #Vlans
  path('vlan/',views.vlan_tab,name='vlan'), #va afficher le tableau des vlans

  #ports
  path('port/',views.port_tab,name='port'), #va afficher le tableau des ports

  #Modeles
  path('modele/',views.modele_tab,name='modele'), #va afficher le tableau des modeles

  #gestion_user
  path('utilisateurs/',views.register_super_user,name='users'),
]
