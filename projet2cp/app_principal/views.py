<<<<<<< HEAD
from email import message
from django.shortcuts import redirect, render
=======

from django.shortcuts import render
>>>>>>> 8fdf46e582e86a59c2002673587197bbbfed6512
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
<<<<<<< HEAD
from .forms import switchform, vlanform, switchConfigForm, modeleform
from .models import switch, vlan, Port, ModeleSwitch
from django.contrib import messages
=======
from .forms import switchform, vlanform, switchConfigForm
from .models import switch, vlan, Port
>>>>>>> 8fdf46e582e86a59c2002673587197bbbfed6512


def ajoutswitch(request):

        form = switchform(request.POST or None)
        if request.method == 'POST':
                if form.is_valid():
                        s=form.save()
                        form.save()
                        id=s.id
                        messages.success(request, ('le switch a été creé avec succés!'))  
                        return redirect('app_principal:config_switch', id)
                else:
                        messages.error(request, ('Echec lors de la création, veuillez réessayer une autre fois.')) 
        context = {'form':form, 'choix':'switch','operation':'Ajout',}
        return render (request ,'app_principal/form_validation.html',context)

def ajoutvlan(request):

        form=vlanform()

        if request.method == 'POST':
                form = vlanform(request.POST)
                if form.is_valid():
                        form.save()
        context = {'form':form, 'choix':'vlan','operation':'Ajout',}
        return render (request ,'app_principal/form_validation.html',context)



def switchConfig(request, switch_id):
    s = get_object_or_404(switch, id=switch_id)
    if request.method == 'POST': #si le switch d'id = switch_id n'existe pas on renvoie 404
        form= switchConfigForm(request.POST,instance=s)

        if form.is_valid():
            form.save()
            if s.etat==switch.passif:
                s.etat=switch.actif
                s.save()
            return redirect('app_principal:switch')
        
            # configuration du `switch` existant dans la base de données
            # redirect vers le form de ports---à faire
        
    else:
        form = switchConfigForm(instance=s)
    return render(request,
                'app_principal/form_validation.html',
                {'form':form, 'choix':s.nom,'operation':'Configuration',})	
        
        

def switchtab(request):
        cols_principales=['nom','bloc','local','armoire','Cascade depuis']
        cols_detail=['Adresse MAC','Numero de Serie',"Numero d'inventaire","Date d'achat",'Marque','Modèle']
        switchs = switch.objects.all()
        context={'objet':'switchs','objets':switchs,'colsp':cols_principales,'colsd':cols_detail,}
        return render(request, 'app_principal/offictable.html',context)

def vlan_tab(request):
        cols_principales=['num_Vlan ','nom','ip','masque','passerelle']
        cols_detail=[]
        vlans = vlan.objects.all()
        context={'objet':'vlans','objets':vlans,'colsp':cols_principales,'colsd':cols_detail,}
        return render(request, 'app_principal/offictable.html',context)

def port_tab(request):
        cols_principales=['num_port','type_port','etat','vlan_associe','elm_suiv']
        cols_detail=[]
        ports = Port.objects.all()
        context={'objet':'ports','objets':ports,'colsp':cols_principales,'colsd':cols_detail,}
        return render(request, 'app_principal/offictable.html',context)

def modele_tab(request):
        cols_principales=['nbr_port','nbr_port_SFP','nbr_port_GE','nbr_port_FE']
        cols_detail=[]
        modeles = ModeleSwitch.objects.all()
        context={'objet':'modèles','objets':modeles,'colsp':cols_principales,'colsd':cols_detail,}
        return render(request, 'app_principal/offictable.html',context)