# Generated by Django 2.1.7 on 2020-02-28 22:51

import account.utils.fields
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personnel', '0001_initial'),
        ('shop', '0017_auto_20190607_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', account.utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', account.utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('item', models.CharField(max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('locked', models.BooleanField(default=False)),
                ('locker', models.CharField(max_length=25)),
                ('notes', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'ordering': ('locked', '-date'),
            },
        ),
        migrations.CreateModel(
            name='ExpenditureType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', account.utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', account.utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'ordering': ('name', '-created'),
            },
        ),
        migrations.CreateModel(
            name='MonthCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', account.utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', account.utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('personnel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='balance_creator', to='personnel.Personnel')),
            ],
            options={
                'ordering': ('-year', '-month'),
            },
        ),
        migrations.AddField(
            model_name='expenditure',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.ExpenditureType'),
        ),
        migrations.AddField(
            model_name='expenditure',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Job'),
        ),
        migrations.AddField(
            model_name='expenditure',
            name='personnel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='personnel.Personnel'),
        ),
    ]
