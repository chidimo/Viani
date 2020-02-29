from decimal import Decimal

from django.db import models
from django.shortcuts import reverse
from django.utils.timezone import now

from shop.models import Job
from personnel.models import Personnel

from .utils.models import TimeStampedModel


class Revenue(TimeStampedModel):
    date = models.DateField(default=now)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    locked = models.BooleanField(default=False)
    locker = models.CharField(max_length=25)
    notes = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ('locked', '-date')

    def __str__(self):
        return f'Rev: {self.amount}'

    def get_absolute_url(self):
        return reverse('bet9ja:revenues')

    def get_object_url(self):
        return reverse('bet9ja:revenue_detail', kwargs={'pk': self.id})


class ExpenditureType(TimeStampedModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ('name', '-created')

    def __str__(self):
        return f'Etype: {self.name.title()}'

    def get_absolute_url(self):
        return reverse('account:expenditure_types')


class Expenditure(TimeStampedModel):
    date = models.DateField(default=now)
    item = models.CharField(max_length=50, default='some-item')
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'))

    locked = models.BooleanField(default=False)
    locker = models.CharField(max_length=25)
    personnel = models.ForeignKey(
        Personnel, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        ExpenditureType, null=True, on_delete=models.SET_NULL)
    notes = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ('locked', '-date')

    def __str__(self):
        return f'Exp: {self.item}-{self.amount}'

    def get_absolute_url(self):
        return reverse('account:expenditures')

    def get_object_url(self):
        return reverse('account:expenditure_detail', kwargs={'pk': self.id})


class MonthCheck(TimeStampedModel):
    year = models.IntegerField()
    month = models.IntegerField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    personnel = models.ForeignKey(
        Personnel, null=True, on_delete=models.SET_NULL, related_name='balance_creator')

    class Meta:
        ordering = ('-year', '-month')
