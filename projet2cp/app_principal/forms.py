from django import forms
from .models import switch, vlan, Port, ModeleSwitch
from django.shortcuts import render, redirect

	


class switchform(forms.ModelForm):

    class Meta: 
        model=switch

        fields = ['nom','mac','inventaire','serie','marque','modele','date_achat']

        

    class Media:
        css= 'static/form.css'

class switchConfigForm(forms.ModelForm):
    
    class Meta: 
        model=switch

        fields = ['bloc','local','armoire','preced']

        #widgets = {
        #    'Vlans_associe': forms.Select(attrs={}),
        #}


class vlanform(forms.ModelForm):
    
    class Meta:
        model = vlan
        fields = "__all__"   
        
class portform(forms.ModelForm):
    
    class Meta:
        model = Port
        fields = "__all__"   
         

    
           





        
        # custom validation for the name field
        
        
       

