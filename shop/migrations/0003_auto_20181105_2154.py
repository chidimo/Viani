# Generated by Django 2.1.3 on 2018-11-05 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20181105_2028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ('completion_status', 'customer', '-created')},
        ),
        migrations.AddField(
            model_name='job',
            name='completion_status',
            field=models.BooleanField(default=False),
        ),
    ]