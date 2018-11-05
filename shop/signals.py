from decimal import Decimal

# from django.db.models import F
from django.db.models.signals import pre_save, pre_delete, post_save#, post_delete
from django.dispatch import receiver

from personnel.models import Personnel
from .models import Job

@receiver(post_save, sender=Job)
def update_expense_payment_profit(sender, instance, **kwargs):
    pass

    
    # personnel = instance.personnel
    # total_sales_amount = instance.total_sales_amount

    # remitted_amount = Decimal('0.00')

    # try:
    #     remitted_amount += instance.cash.amount
    # except AttributeError:
    #     pass

    # try:
    #     remitted_amount += instance.bank.amount
    # except AttributeError:
    #     pass

    # try:
    #     remitted_amount += instance.pos.amount
    # except AttributeError:
    #     pass

    # try:
    #     remitted_amount += instance.winning.amount
    # except AttributeError:
    #     pass

    # try:
    #     personnel.balance = personnel.balance - (total_sales_amount - remitted_amount)
    # except TypeError:
    #     personnel.balance = Decimal('0.00') - (total_sales_amount - remitted_amount)
    # personnel.save(update_fields=['balance'])
