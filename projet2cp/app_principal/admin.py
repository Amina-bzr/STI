from django.contrib import admin
from .models import ModeleSwitch, switch, vlan, Port
# Register your models here.
admin.site.register(switch),
admin.site.register(vlan),
admin.site.register(Port),
admin.site.register(ModeleSwitch)
