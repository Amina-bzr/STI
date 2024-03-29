# Generated by Django 4.0.3 on 2022-03-31 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_principal', '0004_switch_etat'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModeleSwitch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nbr_port', models.PositiveIntegerField(default=0)),
                ('nbr_port_FE', models.PositiveIntegerField(default=0)),
                ('nbr_port_GE', models.PositiveIntegerField(default=0)),
                ('nbr_port_SFP', models.PositiveIntegerField(default=0)),
                ('premier_port_FE', models.PositiveIntegerField(default=1)),
                ('premier_port_GE', models.PositiveIntegerField(default=1)),
                ('premier_port_SFP', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='switch',
            name='nbr_port',
        ),
        migrations.RemoveField(
            model_name='switch',
            name='nbr_port_FE',
        ),
        migrations.RemoveField(
            model_name='switch',
            name='nbr_port_GE',
        ),
        migrations.RemoveField(
            model_name='switch',
            name='nbr_port_SFP',
        ),
        migrations.AlterField(
            model_name='port',
            name='elm_suiv',
            field=models.CharField(max_length=100, verbose_name='Cascade vers'),
        ),
        migrations.AlterField(
            model_name='port',
            name='etat',
            field=models.CharField(choices=[('defectueux', 'Defectueux'), ('relié', 'Relié'), ('non_utilisé', 'Non utilisé')], default='non_utilisé', max_length=50),
        ),
        migrations.AlterField(
            model_name='port',
            name='num_port',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='port',
            name='type_port',
            field=models.CharField(choices=[('FE', 'FE'), ('GE', 'GE'), ('SFP', 'SFP')], max_length=10),
        ),
        migrations.AlterField(
            model_name='port',
            name='vlan_associe',
            field=models.CharField(max_length=50, verbose_name='VLAN associé'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='date_achat',
            field=models.DateTimeField(blank=True, null=True, verbose_name="Date d'achat"),
        ),
        migrations.AlterField(
            model_name='switch',
            name='inventaire',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='mac',
            field=models.CharField(max_length=17, unique=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='marque',
            field=models.CharField(default='Cisco', max_length=50),
        ),
        migrations.AlterField(
            model_name='switch',
            name='modele',
            field=models.CharField(max_length=40, verbose_name='Modèle'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='nom',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='preced',
            field=models.CharField(blank=True, max_length=50, verbose_name='Cascade depuis'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='serie',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
