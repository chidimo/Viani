# Generated by Django 2.1.3 on 2018-11-05 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_squashed_0011_auto_20181105_2006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='completion',
        ),
        migrations.RemoveField(
            model_name='job',
            name='start',
        ),
    ]
