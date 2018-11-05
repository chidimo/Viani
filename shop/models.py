
from django.utils import timezone
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.core.validators import RegexValidator

from personnel.models import Personnel

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

    def __str__(self):
        return 'C: {} {}'.format(self.first_name.title(), self.last_name.title())

    def get_absolute_url(self):
        return reverse('shop:customer_index')

class Job(Company):

    NOT_STARTED = 'not started'
    QUARTER = 'quarter'
    HALF = 'halfway done'
    SEMI = 'almost done'
    DONE = 'completed'

    status_choices = ((NOT_STARTED, 'Not started'), (QUARTER, 'Starting'), (HALF,  'Halfway done'), (SEMI, 'Almost done'), (DONE, 'Done'))
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start = models.DateField(default=timezone.now)
    completion = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=status_choices, default='not started')
    short_description = models.CharField(max_length=30)
    long_description = models.CharField(max_length=500, blank=True)
    notes = models.CharField(max_length=500, blank=True, null=True)

    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return "Job: {}".format(self.short_description.title())

    def get_absolute_url(self):
        return reverse('shop:job_index')

    # def total_expense(self):
    #     exp = self.cashflow_set.filter(category__name='expense').aggregate(sum_exp=Sum('amount'))['sum_exp']
    #     if exp is None:
    #         return 0
    #     else:
    #         return exp

    # def total_payment(self):
    #     pay = self.cashflow_set.filter(category__name='payment').aggregate(sum_pay=Sum('amount'))['sum_pay']
    #     if pay is None:
    #         return 0
    #     else:
    #         return pay

    # def profit(self):
    #     try:
    #         return self.total_payment() - self.total_expense()
    #     except TypeError:
    #         return 0

    def save(self, *args, **kwargs):
        exp = self.cashflow_set.filter(category__name='expense').aggregate(sum_exp=Sum('amount'))['sum_exp']
        pay = self.cashflow_set.filter(category__name='payment').aggregate(sum_pay=Sum('amount'))['sum_pay']

        if exp == None:
            exp = 0
        if pay == None:
            pay = 0

        self.total_expense = exp
        self.total_payment = pay
        self.profit = pay - exp - self.discount

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
        ordering = ('job', 'category', 'banked')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:cashflow_index')
