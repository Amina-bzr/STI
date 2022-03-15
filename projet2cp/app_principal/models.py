from django.db import models

# Create your models here.


class switch(models.Model):
    nom = models.CharField(max_length=50)
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    Bloc = models.CharField(max_length=10)
    Armoire = models.CharField(max_length=10)
    IP = models.GenericIPAddressField()
    Inventaire = models.CharField(max_length=50)
    Serie = models.CharField(max_length=20)
    Mac = models.CharField(max_length=17)
    Nbr_port = models.IntegerField(default=0)
    Nbr_port_FE = models.IntegerField(default=0)
    Nbr_port_GE = models.IntegerField(default=0)
    Nbr_port_SFP = models.IntegerField(default=0)
    # l'element qui precede le switch (le nom du switch precendeant ou data center ou routeurs)
    preced = models.CharField(max_length=50)
    Vlans_associe = models.CharField(max_length=500)
    date_achat = models.DateTimeField('date d''achat')


class vlan(models.Model):
    num_Vlan = models.IntegerField()
    nom = models.CharField(max_length=50)
    Ip = models.GenericIPAddressField()
    Masque = models.CharField(max_length=50)
    Passerelle = models.GenericIPAddressField()


class Port(models.Model):
    Inventaire = models.CharField(max_length=50)
    num_port = models.IntegerField()
    type_port = models.CharField(max_length=50)
    etat = models.CharField(max_length=50)
    vlan_associe = models.CharField(max_length=50)
    elm_suiv = models.CharField(max_length=100)
    # l'elment au quel le port est relié(prise, switch, point d'accès)
