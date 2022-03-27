from django.urls import path
#from .views import viewName

from .import views

app_name="app_principal"

urlpatterns = [
  #path('switch/',views.index,name='switch'), #va afficher le tableau du switch
  path('switch/ajout',views.ajoutswitch,name='add'),
  path('vlan/ajout',views.ajoutvlan,name='add'),
  path('switch/<int:switch_id>/modifier',views.modifierswitch,name='add'),
]
