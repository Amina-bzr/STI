from base64 import urlsafe_b64encode
from email import message
from multiprocessing import context
from queue import LifoQueue
from warnings import catch_warnings
from django.contrib.sites.shortcuts import get_current_site
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as authlogin
from django.contrib.auth.forms import UserCreationForm
from .forms import EditUserPermissionsForm, switchform, vlanform, switchConfigForm, modeleform, CreateSuperUserForm, CreateUserForm, modeleform, CreateSuperUserForm, portform
from .models import switch, vlan, Port, ModeleSwitch
from django.contrib import messages
from django.contrib.auth import decorators
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group, Permission
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist


def acul(request):
    return render(request, 'app_principal/accumm.html')


def servicepage(request):
    return render(request, 'app_principal/service.html')

# User Register


def register(request):
    form = UserCreationForm
    if request.method == 'POST':
        regForm = UserCreationForm(request.POST)
        if regForm.is_valid():
            regForm.save()
            messages.success(request, 'User has been registered.')
    return render(request, 'app_principal/register.html', {'form': form})


def profil(request):
    return render(request, 'app_principal/Profil-user.html')


''' def user_of_stores(user):
	if user.is_authenticated() and user.has_perm("stores.change_store"):
		return True
	else:
		return False

		@user_passes_test(user_of_stores)
'''
# @permission_required('app_principal.add_switch')


def ajoutswitch(request):

    form = switchform(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            nom_model = form.cleaned_data['modele']
            try:
                modele = ModeleSwitch.objects.get(nom=nom_model)
            except ObjectDoesNotExist:
                messages.warning(
                    request, ("Le modele que vous avez introduit n'existe pas veuillez d'abord le créer"))
            else:
                s = form.save()
                form.save()
                id = s.id
                messages.success(
                    request, ('le switch a été creé avec succés!'))
                # return redirect('app_principal:config_switch', id)

                nb_port = modele.nbr_port

                for i in range(1, nb_port+1):
                    if((modele.premier_port_FE <= i) and (i < modele.premier_port_FE+modele.nbr_port_FE)):
                        s.port_set.create(
                            num_port=i, etat=Port.nonutilise, type_port=Port.fe)

                    elif((modele.premier_port_GE <= i) and (i < modele.premier_port_GE+modele.nbr_port_GE)):
                        s.port_set.create(
                            num_port=i, etat=Port.nonutilise, type_port=Port.ge)
                    elif((modele.premier_port_SFP <= i) and (i < modele.premier_port_SFP+modele.nbr_port_SFP)):
                        s.port_set.create(
                            num_port=i, etat=Port.nonutilise, type_port=Port.sfp)

                return redirect('app_principal:config_switch', id)
        else:
            messages.error(
                request, ('Echec lors de la création, veuillez réessayer une autre fois.'))
    context = {'form': form, 'choix': 'switch', 'operation': 'Ajout', }
    return render(request, 'app_principal/form_validation.html', context)


# @permission_required('app_principal.add_vlan')
def plus_info_switch(request,switch_id):
    s=switch.objects.get(id=switch_id)
    context={'objet':s,}
    return render(request, 'app_principal/plus_info.html', context)

def ajoutvlan(request):

    form = vlanform(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
    context = {'form': form, 'choix': 'vlan', 'operation': 'Ajout', }
    return render(request, 'app_principal/form_validation.html', context)

# @permission_required('app_principal.change_switch')


def ajout_modele(request):

    form = modeleform(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,('Modèle créé avec succés!'))
        else:
            messages.warning(request,('Echec lors de la création, veuillez réessayer une autre fois.'))
    context = {'form': form, 'choix': 'modele', 'operation': 'Ajout', }
    return render(request, 'app_principal/form_validation.html', context)


def switchConfig(request, switch_id):
    s = get_object_or_404(switch, id=switch_id)
    if request.method == 'POST':  # si le switch d'id = switch_id n'existe pas on renvoie 404
        form = switchConfigForm(request.POST, instance=s)

        if form.is_valid():
            form.save()
            if s.etat == switch.passif:
                s.etat = switch.actif
                s.save()
            return redirect('./port_tab/', id)
            # configuration du `switch` existant dans la base de données
            # redirect vers le form de ports---à faire

    else:
        form = switchConfigForm(instance=s)
    return render(request,
                  'app_principal/form_validation.html',
                  {'form': form, 'choix': s.nom, 'operation': 'Configuration', })


# # @permission_required('app_principal.change_switch')
def portConfig(request, switch_id, port_num):
    s = get_object_or_404(switch, id=switch_id)
    p = s.port_set.get(num_port=port_num)

    if request.method == 'POST':  # si le switch d'id = switch_id n'existe pas on renvoie 404
        form = portform(request.POST)

        if form.is_valid():

            p.type_port = form.cleaned_data["type_port"]
            p.etat = form.cleaned_data["etat"]
            p.vlan_associe = form.cleaned_data["vlan_associe"]
            p.nom_suiv = form.cleaned_data["nom_suiv"]
            p.type_suiv = form.cleaned_data["type_suiv"]
            p.save()
            s=p.switch
            if not p.vlan_associe in s.vlans:
                s.vlans = s.vlans + p.vlan_associe + " / "
                s.save()
                print(p.vlan_associe)

            return redirect('../port_tab/', switch_id)
    else:
        form = portform(instance=p)

    return render(request,
                  'app_principal/form_validation.html',
                  {'form': form, 'choix': 'Port', 'operation': 'Configuration', })


# def portConfig(request, switch_id, id):

#     form = portform(request.POST or None)

#     return render(request,
#                   'app_principal/form_validation.html',
#                   {'form': form, 'choix': Port, 'operation': 'Configuration', })

# @permission_required('app_principal.view_switch')


def switchtab(request):
    if request.method == 'POST':
        ids_selectionnes = [box[10:] for box in request.POST.keys() if box.startswith("selection_")]
        switchs_selectiones= switch.objects.filter(id__in=ids_selectionnes)
        for sw in switchs_selectiones.all():
            sw.etat = switch.reforme
            sw.bloc = "reformé"
            sw.local = "reformé"
            sw.armoire = "magazin"
            sw.preced = "pas en cascade"
            sw.vlans="Aucun"
            sw.save()
    switchs= switch.objects.all()
    cols_principales = ['nom', 'bloc', 'local', 'armoire', 'Cascade depuis', 'vlans']
    cols_detail = ['Adresse MAC', 'Numero de Serie',
                     "Numero d'inventaire", "Date d'achat", 'Marque', 'Modèle', 'password']
    context = {'objet': 'switchs', 'objets': switchs,
               'colsp': cols_principales, 'colsd': cols_detail, }
    return render(request, 'app_principal/offictable.html', context)


# @permission_required('app_principal.view_vlan')


def vlan_tab(request):
    cols_principales = ['num_Vlan ', 'nom', 'ip', 'masque', 'passerelle']
    cols_detail = []
    vlans = vlan.objects.all()
    context = {'objet': 'vlans', 'objets': vlans,
               'colsp': cols_principales, 'colsd': cols_detail, }
    return render(request, 'app_principal/offictable.html', context)

# @permission_required('app_principal.view_port')


def port_tab(request, switch_id):
    switch_nom=switch.objects.get(id=switch_id).nom
    cols_principales = ['Numero du port', 'Type du port',
                        'Etat', 'Local','Vlan associé', "Type de l'appareil suivante", "nom de l'appareil suivante"]
    cols_detail = []
    # ports = Port.objects.all()
    Ports = Port.objects.filter(switch=switch_id)
    context = {'objet': 'ports', 'objets': Ports,
               'colsp': cols_principales, 'colsd': cols_detail, 'switch_nom':switch_nom,}
    return render(request, 'app_principal/offictable.html', context)

# @permission_required('app_principal.view_modele')


def modele_tab(request):
    cols_principales = ['nom', 'nbr_port', 'nbr_port_FE',
                        'nbr_port_GE', 'nbr_port_SFP', ' premier_port_FE', 'premier_port_GE', ' premier_port_SFP']
    cols_detail = []
    modeles = ModeleSwitch.objects.all()
    context = {'objet': 'modèles', 'objets': modeles,
               'colsp': cols_principales, 'colsd': cols_detail, }
    return render(request, 'app_principal/offictable.html', context)


def login(request):
    return render(request, 'app_principal/login.html')


def profil(request):
    return render(request, 'app_principal/Profil-user.html')

def gestion_user(request):
        users=User.objects.all()        
        if request.method == 'POST': 
                ids_selectionnes = [box[10:] for box in request.POST.keys() if box.startswith("selection_")]
                users_selectiones= User.objects.filter(id__in=ids_selectionnes)
                for user in users_selectiones.all():
                        user.is_active = False        
                        user.save()
            
        context={'users':users,}
        return render(request, 'app_principal/gestionuser.html',context)

def corbeille(request):
        users=User.objects.all()        
        context={'users':users,}
        return render(request, 'app_principal/corbeille.html',context)


def activer_user(request, user_id):
        user = User.objects.get(pk=user_id)
        user.is_active=True
        user.save()
        messages.success(request, ("l'utilisateur "+user.username+" a été activé avec succés!"))
        return redirect('app_principal:corbeille')		


def formprofil(request):
    return render(request, 'app_principal/form_user.html')


def register_super_user(request):
        form=CreateSuperUserForm(request.POST or None)
        if request.method == 'POST': #ladmin a introduit lemail
                
                if form.is_valid():
                        password=get_random_string(length=10)
                        form.password1 = password
                        form.password2=form.password1
                        try:
                                username=form.email_clean()
                        except ValidationError:
                                messages.warning(request,("cet email existe déja"))
                        else:
                                form.username =username
                                form.save()
                                messages.success(request,("Un nouveau superutilisateur a été creé avec succés!"))   
                                user=User.objects.get(email=form.cleaned_data["email"])
                                user.is_superuser=True #on le rend un superutilisateur
                                user.is_active=True #il doit confirmer son email
                                user.save() #on sauvegarde l'user dans la bdd
                                #envoie d'un email

                                #current_site = get_current_site(request)
                                #domain = current_site.domain #le domaine de l'appliquation web
                                
                                context = { #contexte à passer dans l'html
                                'user': user,
                                'password':password,
                                }
                                msg_html = render_to_string('app_principal/registration/mail_activation_changement_passwd.html', context)
                                msg=EmailMultiAlternatives( 
                                        'Bienvenue sur STI esi !',
                                        msg_html,
                                        settings.EMAIL_HOST_USER,
                                        [str(user.email)],
                                ) 
                                msg.content_subtype = "html" #rendre le html comme principal
                                i=msg.send() #returns  si l'email a été envoyé, 0 sinon #gaierror exception si pas de cnx
                                if i==1:
                                        messages.success(request,('un email de confirmation a été envoyé.'))
                                if i==0:
                                        messages.warning(request,('email pas envoyé.'))
                                
                else:
                        messages.warning(request,("Echec! l'utilisateur n'a pas été creé."))            
               
        return render(request,'app_principal/create_super_user.html',{'form':form})	

def register_user(request):
        form=CreateUserForm(request.POST or None)
        if request.method == 'POST': #ladmin a introduit lemail
                
                if form.is_valid():
                        password=get_random_string(length=10)
                        form.password1 = password
                        form.password2=form.password1
                        try:
                                username=form.email_clean()
                        except ValidationError:
                                messages.warning(request,("cet email existe déja"))
                        else:
                                form.username =username
                                form.save()
                                messages.success(request,("Un nouveau utilisateur a été creé avec succés!"))   
                                user=User.objects.get(email=form.cleaned_data["email"])
                                user.is_superuser=False #on le rend un superutilisateur
                                user.is_active=True #il doit confirmer son email
                                for group in form.cleaned_data['permissions']:
                                        user_group = Group.objects.get(name=group) 
                                        user.groups.add(user_group)
                                user.save() #on sauvegarde l'user dans la bdd
                                #envoie d'un email

                                #current_site = get_current_site(request)
                                #domain = current_site.domain #le domaine de l'appliquation web
                                
                                context = { #contexte à passer dans l'html
                                'user': user,
                                'password':password,
                                }
                                msg_html = render_to_string('app_principal/registration/mail_activation_changement_passwd.html', context)
                                msg=EmailMultiAlternatives( 
                                        'Bienvenue sur STI esi !',
                                        msg_html,
                                        settings.EMAIL_HOST_USER,
                                        [str(user.email)],
                                ) 
                                msg.content_subtype = "html" #rendre le html comme principal
                                i=msg.send() #returns  si l'email a été envoyé, 0 sinon #gaierror exception si pas de cnx
                                if i==1:
                                        messages.success(request,('un email de confirmation a été envoyé.'))
                                if i==0:
                                        messages.warning(request,('email pas envoyé.'))
                                
                else:
                        messages.warning(request,("Echec! l'utilisateur n'a pas été creé."))            
               
        return render(request,'app_principal/form-creation-user.html',{'form':form,'operation':'Ajout','choix':'utilisateur'})

def modif_permissions_user(request, user_id):
        form=EditUserPermissionsForm(request.POST or None)
        user=get_object_or_404(User,id=user_id)
        if request.method == 'POST': #ladmin a introduit les nouvelles permissions
                if form.is_valid(): 
                        user.groups.clear() 
                        for group in form.cleaned_data['permissions']:
                                user_group = Group.objects.get(name=group) 
                                user.groups.add(user_group)
                        user.save()
                        messages.success(request,("permissions modifiées avec succés!"))                
                else:
                        messages.warning(request,("Echec! les permissions n'ont pas été modifiées."))            
               
        return render(request,'app_principal/modif_user_permissions.html',{'form':form,'user':user,})
    

def connecter(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            authlogin(request, user)
            return redirect('app_principal:switch')
        else:
            messages.success(
                request, ("There Was An Error Logging In, Try Again..."))
            return redirect('app_principal:login')

    else:
        return render(request, 'app_principal/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('app_principal:vlan')
