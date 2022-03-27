from django import forms
from .models import switch, vlan, Port

class switchform(forms.ModelForm):

    class Meta: 
        model=switch

        fields = "__all__"

        #widgets = {
        #    'Vlans_associe': forms.Select(attrs={}),
        #}

class vlanform(forms.ModelForm):
    class Meta: 
        model=vlan

        fields = "__all__"
