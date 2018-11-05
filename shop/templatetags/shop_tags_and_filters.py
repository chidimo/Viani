from decimal import Decimal

from django import template
from django.db.models import Sum, F

register = template.Library()

@register.filter()
def summ_values(query_set):
    summ = query_set.aggregate(sum_values=Sum('value'))
    return summ['sum_values']

@register.filter()
def summ_discounts(query_set):
    summ = query_set.aggregate(sum_discounts=Sum('discount'))
    return summ['sum_discounts']

@register.filter()
def summ_total_expenses(query_set):
    summ = query_set.aggregate(sum_total_expenses=Sum('total_expense'))
    return summ['sum_total_expenses']

@register.filter()
def summ_total_payments(query_set):
    summ = query_set.aggregate(sum_total_payments=Sum('total_payment'))
    return summ['sum_total_payments']

@register.filter()
def summ_profits(query_set):
    summ = query_set.aggregate(sum_profits=Sum('profit'))
    return summ['sum_profits']
