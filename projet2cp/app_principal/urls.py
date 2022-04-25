



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

]
