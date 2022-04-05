# Generated by Django 4.0.3 on 2022-04-04 15:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_principal', '0010_alter_switch_date_achat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='date_achat',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.RegexValidator('^/d/d//d/d//d/d/d/d$', message='Veuillez respecter le format')], verbose_name="Date d'achat"),
        ),
    ]
