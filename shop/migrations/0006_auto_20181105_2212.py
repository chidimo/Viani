# Generated by Django 2.1.3 on 2018-11-05 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20181105_2207'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ('status', 'customer', '-created')},
        ),
    ]
