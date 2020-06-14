# Generated by Django 3.0.6 on 2020-05-19 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_auto_20200517_2359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsor',
            name='name',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='sponsors',
        ),
        migrations.AddField(
            model_name='match',
            name='player1_winner_pick',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='player2_winner_pick',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='tournament_phase',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sponsor',
            name='tournament',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tournaments.Tournament'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='match',
            name='winner_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Sponsorship',
        ),
    ]