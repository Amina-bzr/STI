from django import forms
from .models import switch, vlan, Port, ModeleSwitch

import datetime

from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm	









	

class switchform(forms.ModelForm):

    class Meta: 
        model=switch

        fields = ['nom','mac','inventaire','serie','marque','modele','date_achat']

        widgets = {
            'nom': forms.TextInput(attrs={'class':'form-control'},),
            'mac': forms.TextInput(attrs={'class':'form-control'},),
            'inventaire': forms.TextInput(attrs={'class':'form-control'},),
            'serie': forms.TextInput(attrs={'class':'form-control'},),
            'marque': forms.TextInput(attrs={'class':'form-control'},),
            'modele': forms.TextInput(attrs={'class':'form-control'},),
            'date_achat':forms.DateInput(attrs={'placeholder': 'jour/mois/année','class':'form-control',},),
        }


class switchConfigForm(forms.ModelForm):
    
    class Meta: 
        model=switch

        fields = ['bloc','local','armoire','preced']

        widgets = {
            'bloc': forms.TextInput(attrs={'class':'form-control'},),
            'local': forms.TextInput(attrs={'class':'form-control'},),
            'armoire': forms.TextInput(attrs={'class':'form-control'},),
            'preced': forms.TextInput(attrs={'class':'form-control'},),
        }



class vlanform(forms.ModelForm):
    
    class Meta:
        model = vlan
        fields = "__all__" 

        
class portform(forms.ModelForm):
    
    class Meta:
        model = Port
        fields = "__all__"   
        
         

    
class modeleform(forms.ModelForm):
    
    class Meta: 
        model=ModeleSwitch

        fields = "__all__" 

        widgets = {
            'nbr_port': forms.TextInput(attrs={'class':'form-control'},),
            'nbr_port_FE': forms.TextInput(attrs={'class':'form-control'},),
            'nbr_port_GE': forms.TextInput(attrs={'class':'form-control'},),
            'nbr_port_SFP': forms.TextInput(attrs={'class':'form-control'},),
            'premier_port_FE': forms.TextInput(attrs={'class':'form-control'},),
            'premier_port_GE': forms.TextInput(attrs={'class':'form-control'},),
            'premier_port_SFP':forms.TextInput(attrs={'class':'form-control',},),
        }           
        





             

