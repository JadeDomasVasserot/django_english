# Generated by Django 3.2.13 on 2023-03-09 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english_test', '0002_alter_joueur_niveau'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joueur',
            name='niveau',
            field=models.IntegerField(),
        ),
    ]
