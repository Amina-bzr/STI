from django.db import models

# Create your models here.


class Switch(models.Model): #on peut creer les ports d'un switch a partir d'un objet "switch" : switch_objet.port_set.create(num_port=...,type_port=...etc)
    nom = models.CharField(max_length=50)
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    bloc = models.CharField(max_length=10)
    armoire = models.CharField(max_length=10)
    ip = models.GenericIPAddressField()
    inventaire = models.CharField(max_length=50)
    serie = models.CharField(max_length=20)
    mac = models.CharField(max_length=17)
    nbr_port = models.IntegerField(default=0)
    nbr_port_FE = models.IntegerField(default=0)
    nbr_port_GE = models.IntegerField(default=0)
    nbr_port_SFP = models.IntegerField(default=0)
    # l'element qui precede le switch (le nom du switch precendeant ou data center ou routeurs)
    preced = models.CharField(max_length=50)
    Vlans_associe = models.CharField(max_length=500)
    date_achat = models.DateTimeField('date d''achat')

    def __str__(self):
        return self.nom


class Vlan(models.Model):
    num_Vlan = models.IntegerField(default=0)
    nom = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    masque = models.CharField(max_length=50)
    passerelle = models.GenericIPAddressField()

    def __str__(self):
        return self.nom


class Port(models.Model): 
    switch= models.ForeignKey(Switch, on_delete=models.CASCADE) #afin que django va supprimer tous les ports associé à un switch si le switch est supprimé
    num_port = models.IntegerField(default=0)
    type_port = models.CharField(max_length=50)
    etat = models.CharField(max_length=50)
    vlan_associe = models.CharField(max_length=50)
    elm_suiv = models.CharField(max_length=100)
    # l'elment au quel le port est relié(prise, switch, point d'accès)
