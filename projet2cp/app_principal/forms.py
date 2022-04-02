from django import forms
from .models import switch, vlan, Port
from django.utils.translation import gettext_lazy as _
class switchform(forms.ModelForm):

    class Meta: 
        model=switch

        fields = "__all__"

        

class vlanform(forms.ModelForm):
    
    class Meta:
        model = vlan
        fields = "__all__"   
        
class portform(forms.ModelForm):
    
    class Meta:
        model = Port
        fields = "__all__"   
         

    
           





        
        # custom validation for the name field
        
        
       

