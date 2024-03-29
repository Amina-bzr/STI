from unittest.mock import DEFAULT
from django.db import models
from django.contrib.auth.models import User
from pkg_resources import require

# Create your models here.


class switch(models.Model):  # on peut creer les ports d'un switch a partir d'un objet "switch" : switch_objet.port_set.create(num_port=...,type_port=...etc)
    # les choix de quelques listes deroulantes
    passif = 'Passif'
    actif = 'Actif'
    reforme = 'Reformé'
    defectueux= 'Défectueux'

    choix_etat = [
        (defectueux, 'Défectueux'),
        (passif, 'Passif'),
        (reforme, 'Reformé'),
        (actif, 'Actif'),
    ]

    # les attributs de la table des switchs

    nom = models.CharField(max_length=50,unique=True)
    marque = models.CharField(max_length=50, default='Cisco')
    modele = models.CharField(max_length=50)
    bloc = models.CharField(max_length=25, default="pas configuré")
    local = models.CharField(max_length=25, default="magazin")
    armoire = models.CharField(max_length=25, default="pas configuré")
    inventaire = models.CharField(max_length=50, unique=True,)
    serie = models.CharField(max_length=25, unique=True,)
    mac = models.CharField(max_length=25, unique=True,)
    password=models.CharField('Mot de passe',max_length=100,blank=True,
                                  null=True,)
   # nbr_port = models.IntegerField(default=0,)
    # nbr_port_FE = models.IntegerField(default=0,)
    # nbr_port_GE = models.IntegerField(default=0,)
    # nbr_port_SFP = models.IntegerField(default=0,)
    # l'element qui precede le switch (le nom du switch precendeant ou data center ou routeurs)
    preced = models.CharField(
        'Cascade depuis', max_length=50, blank=True, default="pas en cascade")
    date_achat = models.DateField("Date d'achat",
                                  blank=True,
                                  null=True,
                                  
                                  )
    etat = models.CharField(
        max_length=10,
        choices=choix_etat,
        default=passif,
    )
    vlans=models.CharField(
        'VLANs associés', max_length=350, blank=True, default="/ ")

    def __str__(self):
        return self.nom


class vlan(models.Model):
    num_Vlan = models.PositiveIntegerField(default=0,unique=True)
    nom = models.CharField(max_length=50)
    ip = models.GenericIPAddressField(unique=True)
    masque = models.CharField(max_length=50)
    passerelle = models.GenericIPAddressField()
    adresse_reseau = models.GenericIPAddressField()
    switchs = models.CharField(max_length=1000,default="/",blank=True)
    #liste des ports
    def __str__(self):
        return self.nom


class Port(models.Model):

    # les valeurs de la liste deroulante 'etat port'
    defect = 'Défectueux'
    relie = 'Utilisé'
    nonutilise = 'Non utilisé'

    etat_port = [
        (defect, 'Défectueux'),
        (relie, 'Utilisé'),
        (nonutilise, 'Non utilisé'),
    ]

    # les valeurs de la liste deroulante 'type port'
    fe = 'FE'
    ge = 'GE'
    sfp = 'SFP'

    choix_type_port = [
        (fe, 'FE'),
        (ge, 'GE'),
        (sfp, 'SFP'),
    ]

    prise = 'Prise'
    switch = 'Switch'
    poit_A = "Point d'accés"
    imprim = "Imprimante"
    aucun = 'Aucun'
    autre = 'Autre'

    choix_type_suiv = [
        (prise, 'Prise'),
        (switch, 'Switch'),
        (poit_A, "Point d'accés"),
        (imprim, "Imprimante"),
        (aucun, 'Aucun'),
        (autre, 'Autre'),
    ]

    # les attributs de la table

    # afin que django va supprimer tous les ports associé à un switch si le switch est supprimé
    switch = models.ForeignKey(switch, on_delete=models.CASCADE, null=True)
    num_port = models.PositiveIntegerField(default=1)
    local=models.CharField(
        max_length=100,
        default='/',)
    type_port = models.CharField(
        max_length=20,
        choices=choix_type_port,
    )
    etat = models.CharField(
        max_length=50,
        choices=etat_port,
        default=nonutilise)
    vlan_associe = models.CharField(
        'VLAN associé', max_length=50, default= "/")
    nom_suiv = models.CharField(
        "Nom de l'équipement relié", max_length=100, default="Non relié")
    type_suiv = models.CharField(
        "Type de l'équipement relié ", max_length=15, default="Aucun", choices=choix_type_suiv,)
    # l'elment au quel le port est relié(prise, switch, point d'accès)


class ModeleSwitch(models.Model):
    # on propose à l'utilisateur de remplir la table des modeles
    nom = models.CharField('Nom du modèle', max_length=50,
                           default='', unique=True)
    nbr_port = models.PositiveIntegerField(default=0)
    nbr_port_FE = models.PositiveIntegerField(default=0)
    nbr_port_GE = models.PositiveIntegerField(default=0)
    nbr_port_SFP = models.PositiveIntegerField(default=0)
    premier_port_FE=models.PositiveIntegerField(default=1) #on utilise le fait que les ports du meme
    premier_port_GE=models.PositiveIntegerField(default=1) #type sont sequentiels
    premier_port_SFP=models.PositiveIntegerField(default=1)
    #pour automatiquement remplir qlq champs du formulaire des ports et switch

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
  

    def __str__(self):
        return f'{self.user.username} Profile'
    

class Contact(models.Model):
    name = models.CharField(max_length=158)
    email = models.EmailField()
    subject = models.CharField(max_length=158)
    message = models.TextField()

    def __str__(self):
        return self.name


class Historique(models.Model):
    username = models.CharField(max_length=100, blank=True, null=True)
    action = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)