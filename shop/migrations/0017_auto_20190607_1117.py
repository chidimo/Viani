# Generated by Django 2.1.7 on 2019-06-07 10:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20190607_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(code='Not set', message="Please enter a valid phone number in the format '+234**********'", regex='^\\+[0-9]{1,13}$')]),
        ),
    ]
