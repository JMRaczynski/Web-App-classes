# Generated by Django 3.0.6 on 2020-05-19 10:30

import datetime
from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0004_auto_20200519_0225'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='tournament',
            constraint=models.CheckConstraint(check=models.Q(start_date__gt=django.db.models.expressions.F('registration_deadline')), name='check_start_date'),
        ),
        migrations.AddConstraint(
            model_name='tournament',
            constraint=models.CheckConstraint(check=models.Q(registration_deadline__gt=datetime.datetime(2020, 5, 19, 12, 30, 52, 417101)), name='check_registration_deadline'),
        ),
    ]
