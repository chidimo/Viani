# Generated by Django 2.1.3 on 2018-11-05 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20181105_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='notes',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
