# Generated by Django 3.0.6 on 2020-06-14 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0024_auto_20200608_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
