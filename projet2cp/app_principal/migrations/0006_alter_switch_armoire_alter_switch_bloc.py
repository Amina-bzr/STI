# Generated by Django 4.0.3 on 2022-04-01 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_principal', '0005_modeleswitch_remove_switch_nbr_port_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='armoire',
            field=models.CharField(default='pas configuré', max_length=10),
        ),
        migrations.AlterField(
            model_name='switch',
            name='bloc',
            field=models.CharField(default='pas configuré', max_length=10),
        ),
    ]
