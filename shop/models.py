import datetime

from django.utils import timezone
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.core.validators import RegexValidator

from .utils.models import TimeStampedModel

class Company(TimeStampedModel):
    company = models.CharField(max_length=60, default="viani", editable=False)
    address = models.CharField(max_length=200, default="holy cross road, new benin, benin city", editable=False)
    phone = models.IntegerField(blank=True, null=True, editable=False)
    registration = models.CharField(max_length=20, blank=True, null=True, editable=False)
    registration_date = models.DateField(default=timezone.now, editable=False)

    class Meta:
        abstract = True

class Customer(TimeStampedModel):
    ML = "male"
    FM = 'female'
    sex_choices = ((ML, 'Male'), (FM, 'Female'))

    msg = "Please enter a valid phone number in the format '+234**********'"
    validate_contact = RegexValidator(regex=r'^\+[0-9]{1,13}$', message=msg, code='Not set')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True, validators=[validate_contact], default="+2341234567890")
    address = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=10, choices=sex_choices, default='female')

    class Meta:
        ordering = ('sex', 'first_name', 'last_name')

    def __str__(self):
        return f'{self.first_name.title()}, {self.last_name.title()}'

    def get_absolute_url(self):
        return reverse('shop:customer_index')

# class DressType(TimeStampedModel):
#     name = models.CharField(max_length=30, unique=True)

#     def __str__(self):
#         return "DT: {}".format(self.name)

#     def get_absolute_url(self):
#         return reverse('shop:dresstype_index')

class Job(Company):
    status_choices = ((1, 'Started'), (2, "Finished"), (3,  'Delivered'), (4, 'Accepted'))
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.IntegerField(choices=status_choices, default=1)
    description = models.CharField(max_length=30)
    notes = models.CharField(max_length=500, blank=True, null=True)

    start_date = models.DateField(default=datetime.date.today)
    completed = models.DateField(default=datetime.date.today)

    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gross_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ('status', '-start_date', 'customer')

    def __str__(self):
        return f'{self.description.title()}'

    def get_absolute_url(self):
        return reverse('shop:job_index')

    def save(self, *args, **kwargs):
        exp = self.cashflow_set.filter(category__name='expense').aggregate(sum_exp=Sum('amount'))['sum_exp']
        pay = self.cashflow_set.filter(category__name='payment').aggregate(sum_pay=Sum('amount'))['sum_pay']

        if exp == None:
            exp = 0
        if pay == None:
            pay = 0

        self.total_expense = exp
        self.total_payment = pay
        self.gross_profit = pay - exp - self.discount
        return super().save(*args, **kwargs)

class CashFlowType(TimeStampedModel):
    """expense, payment"""
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:cashflowtype_index')

class CashFlow(TimeStampedModel):
    category = models.ForeignKey(CashFlowType, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    banked = models.BooleanField(default=False)
    notes = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ('-created', 'job', 'category', 'banked')

    def __str__(self):
        return "{}-{}".format(self.category.name, self.amount)

    def get_absolute_url(self):
        return reverse('shop:cashflow_index')

# class Expense(TimeStampedModel):
#     """Expenses not directly incurred on a garment"""
#     item_name = models.CharField(max_length=50, blank=True, null=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     notes = models.CharField(max_length=500, blank=True)

#     def __str__(self):
#         return "Exp: {}-{}".format(self.item_name, self.amount)
