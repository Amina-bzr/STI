from unittest.util import _MAX_LENGTH
from django import forms

from .models import Contact, switch, vlan, Port, ModeleSwitch

import datetime

from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class switchform(forms.ModelForm):

    class Meta:
        model = switch

        fields = ['mac', 'inventaire', 'serie',
                  'marque', 'modele', 'date_achat']

        widgets = {
            'mac': forms.TextInput(attrs={'class': 'form-control'},),
            'inventaire': forms.TextInput(attrs={'class': 'form-control'},),
            'serie': forms.TextInput(attrs={'class': 'form-control'},),
            'marque': forms.TextInput(attrs={'class': 'form-control'},),
            'modele': forms.TextInput(attrs={'class': 'form-control'},),
            'date_achat': forms.DateInput(attrs={'placeholder': 'jour/mois/année', 'class': 'form-control', },),
        }


class contactform(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'},),
            'email': forms.EmailInput(attrs={'class': 'form-control'},),
            'subject': forms.TextInput(attrs={'class': 'form-control'},),
            'message': forms.TextInput(attrs={'class': 'form-control'},),
        }


class switchConfigForm(forms.ModelForm):
        class Meta:
            model= switch
            fields = ['nom','etat','password','bloc','local','armoire','preced']

        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'},),
            'password': forms.PasswordInput(attrs={'class': 'form-control'},),
            'bloc': forms.TextInput(attrs={'class': 'form-control'},),
            'local': forms.TextInput(attrs={'class': 'form-control'},),
            'armoire': forms.TextInput(attrs={'class': 'form-control'},),
            'preced': forms.TextInput(attrs={'class': 'form-control'},),
        }


class vlanform(forms.ModelForm):

    class Meta:
        model = vlan
        fields = "__all__"


class portform(forms.ModelForm):

    class Meta:
        model = Port
        fields = ['type_port', 'etat','local', 'vlan_associe', 'type_suiv', 'nom_suiv']
        help_texts = {
            'vlan_associe': "introduire '/' si aucun VLAN est associé à ce port",
        }


class suiv_cherche(forms.Form):
    nom_suiv = forms.CharField(label="Nom de l'équipement (switch, point d'accès...) auquel le port est relié :",max_length=100, required=False)
    type_suiv=forms.CharField(label="type de l'élément (prise,switch,imprimante...)auquel le port est relié:",max_length=100, required=False)
    local = forms.CharField(label='Local auquel le port est relié',required=False)


class modeleform(forms.ModelForm):

    class Meta:
        model = ModeleSwitch

        fields = "__all__"

        widgets = {
            'nbr_port': forms.TextInput(attrs={'class': 'form-control'},),
            'nbr_port_FE': forms.TextInput(attrs={'class': 'form-control'},),
            'nbr_port_GE': forms.TextInput(attrs={'class': 'form-control'},),
            'nbr_port_SFP': forms.TextInput(attrs={'class': 'form-control'},),
            'premier_port_FE': forms.TextInput(attrs={'class': 'form-control'},),
            'premier_port_GE': forms.TextInput(attrs={'class': 'form-control'},),
            'premier_port_SFP': forms.TextInput(attrs={'class': 'form-control', },),
        }


class CreateSuperUserForm(UserCreationForm):

    email = forms.EmailField()
    username = forms.CharField(required=False)
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)

    # pour traiter la donnee entrée par l'utilisateur et voir si elle est correcte
    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        user = User.objects.filter(email=email)
        if user.count():  # voir s'il exite un utilisateur avec cet email dans la base de donnee
            raise forms.ValidationError("Cet email existe déja.")
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            self.username,
            self.email_clean(),
            self.password1,
        )
        return user


class CreateUserForm(UserCreationForm):
    GROUP_CHOICES = [
        ('voir', 'Consulter'),
        ('ajouter', 'Ajouter'),
        ('modifier', 'Modifier/Configurer'),
        ('supprimer', 'Supprimer'),
    ]
    email = forms.EmailField()
    username = forms.CharField(required=False)
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    permissions = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                            choices=GROUP_CHOICES)

    # pour traiter la donnee entrée par l'utilisateur et voir si elle est correcte
    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        user = User.objects.filter(email=email)
        if user.count():  # voir s'il exite un utilisateur avec cet email dans la base de donnee
            raise forms.ValidationError("Cet email existe déja.")
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            self.username,
            self.email_clean(),
            self.password1,
        )
        return user

    # pour traiter la donnee entrée par l'utilisateur et voir si elle est correcte
    def permissions_clean(self):
        group = self.cleaned_data['group'].lower()
        return group


class EditUserPermissionsForm(forms.Form):
    GROUP_CHOICES = [
        ('voir', 'Voir'),
        ('ajouter', 'Ajouter'),
        ('modifier', 'Modifier/Configurer'),
        ('supprimer', 'Supprimer'),
    ]
    permissions = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                            choices=GROUP_CHOICES)

    # pour traiter la donnee entrée par l'utilisateur et voir si elle est correcte
    def permissions_clean(self):
        group = self.cleaned_data['group'].lower()
        return group


class update(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','last_name','first_name']

