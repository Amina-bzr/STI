from email import message
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from .forms import switchform, vlanform, switchConfigForm
from .models import switch, vlan, Port
from django.contrib import messages


def ajoutswitch(request):

        form=switchform()

        if request.method == 'POST':
                form = switchform(request.POST)
                if form.is_valid():
                        form.save()
                else:
                     messages.error(request, "Une erreur s'est produite, veuillez reessayer.")   
                        
        context = {'form':form, 'choix':'switch','operation':'Ajout',}
        return render (request ,'app_principal/mainform.html',context)


def ajoutvlan(request):

        form=vlanform()

        if request.method == 'POST':
                form = vlanform(request.POST)
                if form.is_valid():
                        form.save()
                        
        context = {'form':form, 'choix':'vlan','operation':'Ajout',}
        return render (request ,'app_principal/mainform.html',context)



def switchConfig(request, switch_id):
    s = get_object_or_404(switch, id=switch_id)
    if request.method == 'POST': #si le switch d'id = switch_id n'existe pas on renvoie 404
        form= switchConfigForm(request.POST,instance=s)

        if form.is_valid():
            form.save()
            if s.etat==switch.passif:
                s.etat=switch.actif
                s.save()
            # configuration du `switch` existant dans la base de données
            # redirect vers le form de ports---à faire
        
    else:
        form = switchConfigForm(instance=s)
    return render(request,
                'app_principal/mainform.html',
                {'form':form, 'choix':s.nom,'operation':'Configuration',})	
        
        

def switchtab(request):
        switchs = switch.objects.all()
        context={'switchs':switchs,}
        return render(request, 'app_principal/table_switch.html',context)
