
from django.utils import timezone
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.core.validators import RegexValidator

from personnel.models import Personnel

from utils.models import TimeStampedModel

class Company(TimeStampedModel):
    company = models.CharField(max_length=60, default="viani", editable=False)
    address = models.CharField(max_length=200, default="holy cross road, new benin, benin city", editable=False)
    phone = models.IntegerField(blank=True, null=True, editable=False)
    registration = models.CharField(max_length=20, blank=True, null=True, editable=False)
    registration_date = models.DateField(default=timezone.now, editable=False)

    class Meta:
        abstract = True

class Customer(TimeStampedModel):
    ML = "MALE"
    FM = 'FEMALE'
    sex_choices = ((ML, 'male'), (FM, 'female'))

    msg = "Please enter a valid phone number in the format '+234**********'"
    validate_contact = RegexValidator(regex=r'^\+[0-9]{1,13}$', message=msg, code='Not set')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True, validators=[validate_contact])
    address = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=10, choices=sex_choices, default='female')

    def __str__(self):
        return 'Customer: {} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('/')

class Job(Company):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    start = models.DateField(default=timezone.now)
    completion = models.DateField()
    status = models.DecimalField()
    feedback = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('/')

    def total_expense(self):
        agg = self.jobexpense_set.all.aggregate(sum_exp=Sum('amount'))
        return agg['sum_exp']

    def profit(self):
        return self.value - self.total_expense()

class JobExpense(TimeStampedModel):
    item_name = models.CharField(max_length=50)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField()
