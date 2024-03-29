# Generated by Django 3.2.13 on 2023-03-09 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Joueur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('motDePasse', models.CharField(max_length=20)),
                ('niveau', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Partie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('idJoueur', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='english_test.joueur')),
            ],
        ),
        migrations.CreateModel(
            name='Verbe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baseVerbale', models.CharField(max_length=100)),
                ('preterit', models.CharField(max_length=100)),
                ('participePasse', models.CharField(max_length=100)),
                ('traduction', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ville',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cp', models.CharField(max_length=10)),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reponsePreterit', models.CharField(max_length=100)),
                ('reponseParticipePasse', models.CharField(max_length=100)),
                ('dateEnvoi', models.DateTimeField(auto_now_add=True, verbose_name="date d'envoi")),
                ('dateReponse', models.DateTimeField(auto_now_add=True, verbose_name='date de réponse')),
                ('idPartie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='english_test.partie')),
                ('idVerbe', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='english_test.verbe')),
            ],
        ),
        migrations.AddField(
            model_name='joueur',
            name='idVille',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='english_test.ville'),
        ),
    ]
