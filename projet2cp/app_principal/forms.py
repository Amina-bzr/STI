from django import forms
from .models import switch, vlan, Port, ModeleSwitch
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User, Group
from django.forms.fields import EmailField



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
        
       

class CreateSuperUserForm(UserCreationForm):

    email=forms.EmailField(max_length=20)

    def email_clean(self):  #pour traiter la donnee entrée par l'utilisateur et voir si elle est correcte
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise forms.ValidationError("Cet email existe déja.")  
        return email  

    