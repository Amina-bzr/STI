from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from .forms import switchform, vlanform
from .models import switch, vlan, Port


def ajoutswitch(request):

	form=switchform()

	if request.method == 'POST':
		form = switchform(request.POST)
		if form.is_valid():
			form.save()
			
	context = {'form':form, 'choix':'switch','operation':'Ajout',}
	return render (request ,'app_principal/index.html',context)



def ajoutvlan(request):

	form=vlanform()

	if request.method == 'POST':
		form = vlanform(request.POST)
		if form.is_valid():
			form.save()
			
	context = {'form':form, 'choix':'vlan','operation':'Ajout',}
	return render (request ,'app_principal/index.html',context)



def modifierswitch(request, switch_id):
    s = get_object_or_404(switch, id=switch_id) #si le switch d'id = switch_id n'existe pas on retourne 404
	
    if request.method == 'POST':
        form = switchform(request.POST, instance=s)
        if form.is_valid():
            # mise à jour du `switch` existant dans la base de données
            form.save()
            # redirect vers la page du tableau switch ---à faire
    else:
        form = switchform(instance=s)

    return render(request,
                'app_principal/index.html',
                {'form':form, 'choix':'switch','operation':'Modification',})	
	
	
