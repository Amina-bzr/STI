# Generated by Django 4.0.3 on 2022-04-26 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_principal', '0033_alter_vlan_adresse_reseau'),
    ]

    operations = [
        migrations.AlterField(
            model_name='port',
            name='vlan_associe',
            field=models.CharField(default='Aucun', max_length=50, verbose_name='VLAN associé'),
        ),
    ]
