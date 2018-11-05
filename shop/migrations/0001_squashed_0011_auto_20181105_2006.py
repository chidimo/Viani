# Generated by Django 2.1.3 on 2018-11-05 19:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import shop.utils.fields


class Migration(migrations.Migration):

    replaces = [('shop', '0001_initial'), ('shop', '0002_auto_20181105_1631'), ('shop', '0003_auto_20181105_1803'), ('shop', '0004_auto_20181105_1805'), ('shop', '0005_auto_20181105_1901'), ('shop', '0006_auto_20181105_1926'), ('shop', '0007_auto_20181105_1928'), ('shop', '0008_auto_20181105_1929'), ('shop', '0009_auto_20181105_1930'), ('shop', '0010_auto_20181105_1931'), ('shop', '0011_auto_20181105_2006')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', shop.utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', shop.utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('banked', models.BooleanField(default=False)),
                ('notes', models.CharField(blank=True, max_length=500)),
            ],
            options={
                'ordering': ('banked', 'category'),
            },
        ),
        migrations.CreateModel(
            name='CashFlowType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', shop.utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', shop.utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', shop.utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', shop.utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(blank=True, default='+2341234567890', max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(code='Not set', message="Please enter a valid phone number in the format '+234**********'", regex='^\\+[0-9]{1,13}$')])),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='female', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', shop.utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', shop.utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('company', models.CharField(default='viani', editable=False, max_length=60)),
                ('address', models.CharField(default='holy cross road, new benin, benin city', editable=False, max_length=200)),
                ('phone', models.IntegerField(blank=True, editable=False, null=True)),
                ('registration', models.CharField(blank=True, editable=False, max_length=20, null=True)),
                ('registration_date', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('completion', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('new job', 'New job'), ('started', '25%/ done'), ('halfway', '50%/ done'), ('almost', '75%/ done'), ('completed', '100%/ done')], default='not started', max_length=15)),
                ('short_description', models.CharField(max_length=30)),
                ('long_description', models.CharField(blank=True, max_length=500)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Customer')),
                ('profit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_expense', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_payment', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('notes', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='cashflow',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.CashFlowType'),
        ),
        migrations.AddField(
            model_name='cashflow',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Job'),
        ),
        migrations.AlterModelOptions(
            name='cashflow',
            options={'ordering': ('job', 'category', 'banked')},
        ),
    ]
