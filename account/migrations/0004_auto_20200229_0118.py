# Generated by Django 2.1.7 on 2020-02-29 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_revenue'),
    ]

    operations = [
        migrations.AddField(
            model_name='revenue',
            name='locker',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expenditure',
            name='item',
            field=models.CharField(max_length=50),
        ),
    ]
