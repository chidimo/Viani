# Generated by Django 2.1.7 on 2020-02-28 23:02

import account.utils.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0001_initial'),
        ('account', '0002_auto_20200228_2352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', account.utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', account.utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('locked', models.BooleanField(default=False)),
                ('notes', models.CharField(blank=True, max_length=250)),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personnel.Personnel')),
            ],
            options={
                'ordering': ('locked', '-date'),
            },
        ),
    ]
