# Generated by Django 4.0.3 on 2022-05-18 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_principal', '0038_alter_switch_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Mot de passe'),
        ),
    ]