# Generated by Django 3.0.6 on 2020-05-21 12:04
from datetime import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0020_remove_match_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.now),
            preserve_default=False,
        ),
    ]
