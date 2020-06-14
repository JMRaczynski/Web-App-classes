# Generated by Django 3.0.6 on 2020-05-21 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0022_match_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='player1_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='player 1+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='match',
            name='player2_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='player 2+', to=settings.AUTH_USER_MODEL),
        ),
    ]