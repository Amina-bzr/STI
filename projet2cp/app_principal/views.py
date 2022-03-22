from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Switch, Vlan, Port
from django.template import loader
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

# Create your views here.
def Index(request):
    return HttpResponse("you are welcome")