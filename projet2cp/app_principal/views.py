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
			
	context = {'form':form, 'choix':'switch',}
	return render (request ,'app_principal/index.html',context)



def ajoutvlan(request):

	form=vlanform()

	if request.method == 'POST':
		form = vlanform(request.POST)
		if form.is_valid():
			form.save()
			
	context = {'form':form, 'choix':'vlan',}
	return render (request ,'app_principal/index.html',context)