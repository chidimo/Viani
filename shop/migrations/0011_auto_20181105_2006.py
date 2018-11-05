# Generated by Django 2.1.3 on 2018-11-05 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20181105_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('new job', 'New job'), ('started', '25%/ done'), ('halfway', '50%/ done'), ('almost', '75%/ done'), ('completed', '100%/ done')], default='not started', max_length=15),
        ),
    ]
