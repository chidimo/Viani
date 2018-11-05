# Generated by Django 2.1.3 on 2018-11-05 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20181105_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(blank=True, choices=[('0', 'Not started'), ('25', 'Starting'), ('50', 'Halfway done'), ('75', 'Almost done'), ('100', 'Done')], max_length=15, null=True),
        ),
    ]
