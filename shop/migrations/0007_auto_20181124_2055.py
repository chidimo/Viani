# Generated by Django 2.1.3 on 2018-11-24 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20181107_1209'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ('sex', 'first_name', 'last_name')},
        ),
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ('-start_date', 'status', 'customer')},
        ),
    ]
