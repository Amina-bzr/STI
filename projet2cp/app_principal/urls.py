from django.urls import path
#from .views import viewName

from .import views

app_name="app_principal"

urlpatterns = [
  #path('switch/',views.index,name='switch'),
  path('switch/ajout',views.ajoutswitch,name='add'),
  path('vlan/ajout',views.ajoutvlan,name='add'),
]
