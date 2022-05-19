from base64 import urlsafe_b64encode
from email import message
from urllib import request
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from multiprocessing import context
from django.contrib.sites.shortcuts import get_current_site
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as authlogin
from django.contrib.auth.forms import UserCreationForm
from .forms import EditUserPermissionsForm, contactform, suiv_cherche, switchform, vlanform, switchConfigForm, modeleform, CreateSuperUserForm, CreateUserForm, modeleform, CreateSuperUserForm, portform, update
from .models import switch, vlan, Port, ModeleSwitch, Contact
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth import decorators
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group, Permission
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist



def PageAccueil(request):
    return render(request, 'app_principal/PageAccueil.html')



def servicepage(request):
    return render(request, 'app_principal/service.html')


''' def register(request):
    form = UserCreationForm
    if request.method == 'POST':
        regForm = UserCreationForm(request.POST)
        if regForm.is_valid():
            regForm.save()
            messages.success(request, 'User has been registered.')
    return render(request, 'app_principal/register.html', {'form': form}) '''


# PROFIL-----------------------------------------------------------
@login_required()
def p(request):
    return render(request, 'app_principal/profil.html')


# SWITCH------------------------------------------------------------
@login_required()
@user_passes_test(lambda u: (Group.objects.get(name="ajouter") in u.groups.all()) or u.is_superuser == True, login_url='app_principal:profile')
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
            messages.warning(
                request, ('Echec lors de la création, veuillez réessayer une autre fois.'))
    context = {'form': form, 'choix': 'switch', 'operation': 'Ajout', }
    return render(request, 'app_principal/form_validation.html', context)


@login_required()
@user_passes_test(lambda u: (Group.objects.get(name="voir") in u.groups.all()) or u.is_superuser == True, login_url='app_principal:profile')
def plus_info_switch(request, switch_id):
    s = switch.objects.get(id=switch_id)
    context = {'objet': s, }
    return render(request, 'app_principal/plus_info.html', context)


@login_required()
@user_passes_test(lambda u: (Group.objects.get(name="modifier") in u.groups.all()) or u.is_superuser == True, login_url='app_principal:profile')
def switchConfig(request, switch_id):
    s = get_object_or_404(switch, id=switch_id)
    if request.method == 'POST':  # si le switch d'id = switch_id n'existe pas on renvoie 404
        form = switchConfigForm(request.POST, instance=s)

        if form.is_valid():
            form.save()
            s.bloc=s.bloc.upper()
            s.save()
            #if (s.etat == switch.passif):
            #    #s.etat = switch.actif
            #    s.bloc=s.bloc.upper()
            #    s.save()
            return redirect('./port_tab/', id)
            # configuration du `switch` existant dans la base de données
            # redirect vers le form de ports---à faire

    else:
        form = switchConfigForm(instance=s)
    return render(request,
                  'app_principal/form_validation.html',
                  {'form': form, 'choix': 'switch', 'objet': s.nom, 'operation': 'Configuration', })


@login_required()
@user_passes_test(lambda u: (Group.objects.get(name="voir") in u.groups.all()) or u.is_superuser == True, login_url='app_principal:profile')
def switchtab(request):
    if request.method == 'POST':
        ids_selectionnes = [
            box[10:] for box in request.POST.keys() if box.startswith("selection_")]
        switchs_selectiones = switch.objects.filter(id__in=ids_selectionnes)
        for sw in switchs_selectiones.all():
            sw.etat = switch.reforme
            sw.bloc = "reformé"
            sw.local = "reformé"
            sw.armoire = "magazin"
            sw.preced = "pas en cascade"
            sw.vlans = "/"
            sw.save()
            vls = vlan.objects.all()
            for v in vls :
                if sw.nom in v.switchs: 
                    v.switchs= v.switchs.replace(sw.nom,"")
                    v.switchs= v.switchs.replace("/","",1)
                    v.save()
                    print(v.switchs)
            for port in sw.port_set.all():
                port.etat = Port.nonutilise
                port.vlan_associe = "/"
                port.local = "magazin"
                port.type_suiv = "Aucun"
                port.nom_suiv = "/"
                port.save()
    switchs = switch.objects.all()
    cols_principales = ['nom', 'bloc', 'local',
                        'armoire', 'Cascade depuis', 'VLANs']
    cols_detail = ['Adresse MAC', 'Numero de Serie',
                   "Numero d'inventaire", "Date d'achat", 'Marque', 'Modèle', 'password']
    context = {'objet': 'switchs', 'objets': switchs,
               'colsp': cols_principales, 'colsd': cols_detail, }
    return render(request, 'app_principal/offictable.html', context)


# Recherch view:
@login_required()
@user_passes_test(lambda u: (Group.objects.get(name="voir") in u.groups.all()) or u.is_superuser == True, login_url='app_principal:profile')
def recherche_elem_suiv(request):
    if request.method == 'POST':  # si le switch d'id = switch_id n'existe pas on renvoie 404
        form = suiv_cherche(request.POST)

        if form.is_valid():
            n = form.cleaned_data["nom_suiv"]
            l = form.cleaned_data["local"]
            if n != "":
                port = Port.objects.filter(nom_suiv__iexact=n)
                print(port)
                if port.exists():
                    id = port[:1].get().switch.id
                    return redirect('app_principal:port', id)
                else:
                    messages.warning(
                        request, ('Le nom de cet élément ne figure dans la listes des appariels suivant veillez verrifier le nom.'))
            elif l != "":
                i = 0

                po = []
                port = Port.objects.filter(local__iexact=l)

                for p in port.all():
                    po.insert(i, p)
                    i = i+1

                if len(po) > 0:

                    context = {"switch": po, "len": len(po)}
                    return render(request, 'app_principal/recherche.html', context)
                else:
                    messages.warning(
                        request, ('Le local ne figure dans la listes des appariels suivant veillez verrifier votre saisie.'))

        else:
            messages.warning(
                request, ('Le nom de cet élément ne figure dans la listes des appariels suivant veillez verrifier le nom.'))
    else:
        form = suiv_cherche()

    return render(request,
                  'app_principal/form_validation.html',
                  {'form': form, 'choix': 'Port', 'operation': 'Recherche', })


# MODELE-----------------------------------------------------------
@login_required()
@user_passes_test(lambda u: (Group.objects.get(name="voir") in u.groups.all()) or u.is_superuser == True, login_url='app_principal:profile')
def modele_tab(request):
    cols_principales = ['nom', 'nbr_port', 'nbr_port_FE',
                        'nbr_port_GE', 'nbr_port_SFP', ' premier_port_FE', 'premier_port_GE', ' premier_port_SFP']
    cols_detail = []
    modeles = ModeleSwitch.objects.all()
    context = {'objet': 'modèles', 'objets': modeles,
               'colsp': cols_principales, 'colsd': cols_detail, }
    return render(request, 'app_principal/offictable.html', context)


@login_required()
@user_passes_test(lambda u: (Group.objects.get(name="ajouter") in u.groups.all()) or u.is_superuser == True, login_url='app_principal:profile')
def ajout_modele(request):
    form = modeleform(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, ('Modèle créé avec succés!'))
            return redirect('app_principal:modele')
        else:
            messages.warning(
                request, ('Echec lors de la création, veuillez réessayer une autre fois.'))
    context = {'form': form, 'choix': 'modele', 'operation': 'Ajout', }
    return render(request, 'app_principal/form_validation.html', context)

# PORTS------------------------------------------------------------


@login_required()
@user_passes_test(lambda u: (Group.objects.get(name="modifier") in u.groups.all()) or u.is_superuser == True, login_url='app_principal:profile')
def portConfig(request, switch_id, port_num):
    s = get_object_or_404(switch, id=switch_id)
    p = s.port_set.get(num_port=port_num)
    vls = vlan.objects.all()
    if request.method == 'POST':  # si le switch d'id = switch_id n'existe pas on renvoie 404
        form = portform(request.POST)
        try: #voir si le VLAN existe dans la table des vlans
            nom_vlan=request.POST['vlan_associe']
            if (nom_vlan!='/'):
                v=vlan.objects.get(nom__iexact=nom_vlan)
        except ObjectDoesNotExist:
            messages.warning(request,("Le VLAN que vous avez introduit n'existe pas.. si ce n'est pas une erreur de saisie, veuillez le créer d'habord."))
        else:
               
            if form.is_valid():
                p.type_port = form.cleaned_data["type_port"]
                p.etat = form.cleaned_data["etat"]
                p.vlan_associe = form.cleaned_data["vlan_associe"].capitalize()
                p.nom_suiv = form.cleaned_data["nom_suiv"]
                p.type_suiv = form.cleaned_data["type_suiv"]
                p.local=form.cleaned_data["local"]
                p.save()
                list_vlans= s.port_set.values_list('vlan_associe', flat=True).distinct()
                s.vlans='/ '.join([str(vlan) for vlan in list_vlans if vlan!='/'])
                s.save()
                for v in vls : 
                    if str(v.nom).capitalize() in s.vlans and not s.nom in v.switchs :
                        v.switchs = v.switchs + s.nom + " / "
                        v.save()
                        print(s.nom)
                messages.success(request,('port numero '+str(p.num_port)+' configuré avec succés!'))
                return redirect('../port_tab/', switch_id)
            else:
                messages.warning(request,('echec lors de la configuration, veuillez réessayer une autre fois.'))
    else:
        form = portform(instance=p)

    return render(request,
                  'app_principal/form_validation.html',
                  {'form': form, 'choix': 'Port', 'switch':s, 'operation': 'Configuration', })


@login_required()
@user_passes_test(lambda u: (Group.objects.get(name="voir") in u.groups.all()) or u.is_superuser == True, login_url='app_principal:profile')
def port_tab(request, switch_id):
    switch_nom = switch.objects.get(id=switch_id).nom
    cols_principales = ['Numero du port', 'Type du port',
                        'Etat', 'Local', 'Vlan associé', "Type de l'appareil suivante", "nom de l'appareil suivante"]
    cols_detail = []
    # ports = Port.objects.all()
    Ports = Port.objects.filter(switch=switch_id)
    context = {'objet': 'ports', 'objets': Ports,
               'colsp': cols_principales, 'colsd': cols_detail, 'switch_nom': switch_nom, }
    return render(request, 'app_principal/offictable.html', context)


# GESTION D'UTILISATEURS----------------------------------------------------------------
@login_required()
@user_passes_test(lambda u: u.is_superuser == True, login_url='app_principal:profile')
def gestion_user(request):
    users = User.objects.all()
    if request.method == 'POST':
        ids_selectionnes = [
            box[10:] for box in request.POST.keys() if box.startswith("selection_")]
        users_selectiones = User.objects.filter(id__in=ids_selectionnes)
        for user in users_selectiones.all():
            user.is_active = False
            user.save()

    context = {'users': users, }
    return render(request, 'app_principal/gestionuser.html', context)


@login_required()
@user_passes_test(lambda u: u.is_superuser == True, login_url='app_principal:profile')
def corbeille(request):
    users = User.objects.all()
    context = {'users': users, }
    return render(request, 'app_principal/corbeille.html', context)


@login_required()
@user_passes_test(lambda u: u.is_superuser == True, login_url='app_principal:profile')
def activer_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    messages.success(request, ("l'utilisateur " +
                     user.username+" a été activé avec succés!"))
    return redirect('app_principal:corbeille')


@login_required()
@user_passes_test(lambda u: u.is_superuser == True, login_url='app_principal:profile')
def register_super_user(request):
    form = CreateSuperUserForm(request.POST or None)
    if request.method == 'POST':  # ladmin a introduit lemail

        if form.is_valid():
            password = get_random_string(length=10)
            form.password1 = password
            form.password2 = form.password1
            try:
                username = form.email_clean()
            except ValidationError:
                messages.warning(request, ("cet email existe déja"))
            else:
                form.username = username
                form.save()
                messages.success(
                    request, ("Un nouveau superutilisateur a été creé avec succés!"))
                user = User.objects.get(email=form.cleaned_data["email"])
                user.is_superuser = True  # on le rend un superutilisateur
                user.is_active = True  # il doit confirmer son email
                user.save()  # on sauvegarde l'user dans la bdd
                # envoie d'un email

                #current_site = get_current_site(request)
                # domain = current_site.domain #le domaine de l'appliquation web

                context = {  # contexte à passer dans l'html
                    'user': user,
                    'password': password,
                }
                msg_html = render_to_string(
                    'app_principal/registration/mail_activation_changement_passwd.html', context)
                msg = EmailMultiAlternatives(
                    'Bienvenue sur STI esi !',
                    msg_html,
                    settings.EMAIL_HOST_USER,
                    [str(user.email)],
                )
                msg.content_subtype = "html"  # rendre le html comme principal
                i = msg.send()  # returns  si l'email a été envoyé, 0 sinon #gaierror exception si pas de cnx
                if i == 1:
                    messages.success(
                        request, ('un email de confirmation a été envoyé.'))
                if i == 0:
                    messages.warning(request, ('email pas envoyé.'))

        else:
            messages.warning(
                request, ("Echec! l'utilisateur n'a pas été creé."))

    return render(request, 'app_principal/create_super_user.html', {'form': form})


@login_required()
@user_passes_test(lambda u: u.is_superuser == True, login_url='app_principal:profile')
def register_user(request):
    form = CreateUserForm(request.POST or None)
    if request.method == 'POST':  # ladmin a introduit lemail

        if form.is_valid():
            password = get_random_string(length=10)
            form.password1 = password
            form.password2 = form.password1
            try:
                username = form.email_clean()
            except ValidationError:
                messages.warning(request, ("cet email existe déja"))
            else:
                form.username = username
                form.save()
                messages.success(
                    request, ("Un nouveau utilisateur a été creé avec succés!"))
                user = User.objects.get(email=form.cleaned_data["email"])
                user.is_superuser = False  # on le rend un superutilisateur
                user.is_active = True  # il doit confirmer son email
                for group in form.cleaned_data['permissions']:
                    user_group = Group.objects.get(name=group)
                    user.groups.add(user_group)
                user.save()  # on sauvegarde l'user dans la bdd
                # envoie d'un email

                #current_site = get_current_site(request)
                # domain = current_site.domain #le domaine de l'appliquation web

                context = {  # contexte à passer dans l'html
                    'user': user,
                    'password': password,
                }
                msg_html = render_to_string(
                    'app_principal/registration/mail_activation_changement_passwd.html', context)
                msg = EmailMultiAlternatives(
                    'Bienvenue sur STI esi !',
                    msg_html,
                    settings.EMAIL_HOST_USER,
                    [str(user.email)],
                )
                msg.content_subtype = "html"  # rendre le html comme principal
                i = msg.send()  # returns  si l'email a été envoyé, 0 sinon #gaierror exception si pas de cnx
                if i == 1:
                    messages.success(
                        request, ('un email de confirmation a été envoyé.'))
                if i == 0:
                    messages.warning(request, ('email pas envoyé.'))

        else:
            messages.warning(
                request, ("Echec! l'utilisateur n'a pas été creé."))

    return render(request, 'app_principal/form-creation-user.html', {'form': form, 'operation': 'Ajout', 'choix': 'utilisateur'})


@login_required()
@user_passes_test(lambda u: u.is_superuser == True, login_url='app_principal:profile')
def modif_permissions_user(request, user_id):
    form = EditUserPermissionsForm(request.POST or None)
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':  # ladmin a introduit les nouvelles permissions
        if form.is_valid():
            user.groups.clear()
            for group in form.cleaned_data['permissions']:
                user_group = Group.objects.get(name=group)
                user.groups.add(user_group)
            user.save()
            messages.success(request, ("permissions modifiées avec succés!"))
        else:
            messages.warning(
                request, ("Echec! les permissions n'ont pas été modifiées."))

    return render(request, 'app_principal/modif_user_permissions.html', {'form': form, 'usr': user, })


# AUTHENTIFICATION-------------------------------------------------------------------------
#@user_passes_test(lambda u: u.is_anonymous == True, login_url='app_principal:profile')
def connecter(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            authlogin(request, user)
            return redirect('app_principal:switch')
        else:
            messages.warning(
                request, ("Mot de passe ou nom d'utilisateur invalide, veuillez réessayer une autre fois."))
            return redirect('app_principal:login')

    else:
        return render(request, 'app_principal/login.html', {})


@login_required()
def logout_user(request):
    logout(request)
    messages.success(request, ("Deconnexion faite avec succés!"))
    return redirect('app_principal:login')


class PasswordReset(PasswordResetView):
    template_name = 'app_principal/password/password_reset.html'


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'app_principal/password/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'app_principal/password/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'app_principal/password/password_reset_complete.html'


@login_required()
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Votre mot de asse a été actualisé.")
            return redirect('app_principal:switch')
        else:
            messages.warning(request, "Echec.. veuillez réessayer.")

    else:
        form = PasswordChangeForm(user=request.user)

    context = {
        'form': form,
        'objet':'mot de passe',
        'operation':'changement du ',
    }
    return render(request, 'app_principal/form_validation.html', context)


# CONTACT--------------------------------
def contact(request):
    if request.method == "POST":

        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact.name = name
        contact.email = email
        contact.message = message
        contact.save()
        i=send_mail('Contact Form', message, settings.EMAIL_HOST_USER, [
                  'ka_sebti@esi.dz', 'asma16.sebti@gmail.com'], fail_silently=False)
        if (i==1):
            messages.success(request, ("Merci de nous avoir contacté"))
        else :
            messages.warning(request, ("Echec.. email non envoyé, veuillez réessayer une autre fois."))

    return render(request, 'contact.html')





# VLAN----------------------------------------

@login_required()
@user_passes_test(lambda u: (Group.objects.get(name="voir") in u.groups.all()) or u.is_superuser == True, login_url='app_principal:profile')
def vlan_tab(request):
    cols_principales = ['Vlan ', 'Nom', 'Adresse réseau',
                        'ip', 'Masque Sous Réseau', 'Passerelle', 'Switchs', ' ', ' ']
    cols_detail = []
    vlans = vlan.objects.all()
    context = {'objet': 'vlans', 'objets': vlans,
               'colsp': cols_principales, 'colsd': cols_detail, }
    return render(request, 'app_principal/offictable.html', context)


@login_required()
@user_passes_test(lambda u: (Group.objects.get(name="ajouter") in u.groups.all()) or u.is_superuser == True, login_url='app_principal:profile')
def ajoutvlan(request):

    form = vlanform(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'ce vlan a été ajouté avec succès..!')
            return redirect('/app_principal/vlan')
    context = {'form': form, 'choix': 'vlan', 'operation': 'Ajout', }
    return render(request, 'app_principal/form_validation.html', context)


@login_required()
@user_passes_test(lambda u: (Group.objects.get(name="modifier") in u.groups.all()) or u.is_superuser == True, login_url='app_principal:profile')
def updateVlan(request, id):
    updVlan = get_object_or_404(vlan, id=id)
    initialData = {
        'num_Vlan': updVlan.num_Vlan,
        'nom': updVlan.nom,
        'adresse_reseau': updVlan.adresse_reseau,
        'ip': updVlan.ip,
        'masque': updVlan.masque,
        'passerelle': updVlan.passerelle,
    }
    if request.method == "POST":
        editForm = vlanform(request.POST, instance=updVlan)
        if editForm.is_valid():
            editForm.save()
        messages.success(
            request, 'Les information de ce vlan ont été mis à jour avec succès...!')
        return redirect('/app_principal/vlan')
    editForm = vlanform(initialData)
    context = {'form': editForm, 'choix': 'vlan', 'operation': 'modification'}
    return render(request, 'app_principal/form_validation.html', context)


@login_required()
@user_passes_test(lambda u: (Group.objects.get(name="supprimer") in u.groups.all()) or u.is_superuser == True, login_url='app_principal:profile')
def deleteVlan(request,id):
        swt = switch.objects.all()
        deletVlan = get_object_or_404(vlan,id=id)
        initialData={
           'num_Vlan': deletVlan.num_Vlan ,
           'nom': deletVlan.nom ,
            'adresse_reseau' : deletVlan.adresse_reseau ,
            'ip' : deletVlan.ip ,
            'masque' : deletVlan.masque ,
            'passerelle' : deletVlan.passerelle ,
        }
        form = vlanform(initial=initialData)
        if request.method == 'POST' :
                deletVlan.delete() 
                for s in swt :
                    if str(deletVlan.nom).capitalize() in s.vlans:
                        for x in s.port_set.all():
                            if str(deletVlan.nom).capitalize() in x.vlan_associe:
                                x.vlan_associe='/'
                                x.save()
                        list_vlans= s.port_set.values_list('vlan_associe', flat=True).distinct()
                        s.vlans='/ '.join([str(vlan) for vlan in list_vlans if vlan!='/'])
                        s.save()
                messages.success(request,' ce vlan ont été supprimé avec succès...!')
                return redirect("/app_principal/vlan")
        context={
                'form':form , 'choix':'vlan', 'operation':'supression'
        }
        return render(request,'app_principal/form_validation.html',context)


# STATISTIQUES
def remove_duplicates(duplist):
    noduplist = []
    for element in duplist:
        if element not in noduplist:
            noduplist.append(element)
    return noduplist


@login_required()
def statistique(request):
        labels1 = []
        data1 = []
         
        vlans = vlan.objects.values_list('nom', flat=True)
        for Vlan in vlans:

                nb_ports = Port.objects.filter(vlan_associe__iexact= Vlan).count() 
                
                labels1.append(Vlan)
                data1.append(nb_ports)
             

       
        labels2=[]
        data2 = []

        etats = ['Défectueux','Utilisé','Non utilisé']
        for port in etats:

            etat_port = Port.objects.filter(etat= port ).count() 
                
            labels2.append(port)
            data2.append(etat_port)
             
        labels3=[]
        data3 = []
        types = ['FE','GE','SFP']
        for typ in types:

            Type = Port.objects.filter(type_port= typ ).count() 
                
            labels3.append(typ)
            data3.append(Type)

        labels4=[]
        data4 = []
        etat_switch = ['Défectueux','Passif','Reformé','Actif']
        for etatS in etat_switch:

            nbswitch = switch.objects.filter(etat = etatS  ).count() 
                
            labels4.append(etatS)
            data4.append(nbswitch)  

        labels5=[]
        data5 = []
        Blocs = switch.objects.values_list('bloc', flat=True)
        blocs = remove_duplicates(Blocs)
        for Bloc in blocs:

                queryset = switch.objects.filter(bloc = Bloc).count()
                
                labels5.append(Bloc)
                data5.append(queryset)      

        context =  {
            'labels1': labels1,
            'labels2': labels2,
            'labels2': labels2,
            'labels4': labels4,
            'labels5': labels5,
            'data1': data1,
            'data2': data2,
            'data3': data3,
            'data4': data4,
            'data5': data5,
             }
        return render(request, 'app_principal/statistique.html',context)


def profilUpdate(request):
    if request.method == 'POST':
        u_form = update(request.POST, instance=request.user)

        if u_form.is_valid():
            #user=request.user
            #user.username=u_form.cleaned_data['username']
            #user.email=u_form.cleaned_data['email']
            #user.last_name=u_form.cleaned_data['last_name']
            #user.first_name=u_form.cleaned_data['first_name']
            #user.save()
            u_form.save()
            messages.success(
                request, f'Votre info-personnelles sont mis à jour!')
            return redirect('app_principal:c')

    else:
        u_form = update(instance=request.user)

    context = {
        'form': u_form,
        'operation':'Mdifier',
        'objet':'Infos Personnels',

    }

    return render(request, 'app_principal/form_validation.html', context)