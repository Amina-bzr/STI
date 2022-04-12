



from  django.urls import path
from  .import views
app_name="app_principal"

urlpatterns = [ 
     path('switch/',views.switchtab,name='switch'), #va afficher le tableau des switchs
     path('switch/ajout',views.ajoutswitch,name='add_switch'),
     path('vlan/ajout',views.ajoutvlan,name='add'),

     path('switch/<int:switch_id>/configurer',views.switchConfig,name='config_switch'),


     path('vlan/',views.vlan_tab,name='vlan'), #va afficher le tableau des vlans


     path('port/',views.port_tab,name='port'), #va afficher le tableau des ports

 
     path('modele/',views.modele_tab,name='modele'), #va afficher le tableau des modeles

     path('switch/<int:switch_id>/configurer',views.switchConfig,name='add'),
     path('home',views.home,name='home'),
     path('register/',views.register,name='register'),
    # path('login/',views.login,name='register'),
     path('user/',views.profil,name='add'),
     path('user_form/',views.formprofil,name='add'),
    
    ]

   
	 

    
  





  
