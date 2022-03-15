from django.contrib import admin
from .models import switch, vlan, Port
# Register your models here.
admin.site.register(switch),
admin.site.register(vlan),
admin.site.register(Port)
