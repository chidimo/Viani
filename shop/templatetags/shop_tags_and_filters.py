from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def status_text(value):
    return {1: 'Started', 2: "Finished", 3: 'Delivered', 4: 'Accepted'}[value]

@register.filter()
def summ_values(query_set):
    summ = query_set.aggregate(total=Sum('value'))
    return summ['total']

@register.filter()
def summ_discounts(query_set):
    summ = query_set.aggregate(total=Sum('discount'))
    return summ['total']

@register.filter()
def summ_total_expenses(query_set):
    summ = query_set.aggregate(total=Sum('total_expense'))
    return summ['total']

@register.filter()
def summ_total_payments(query_set):
    summ = query_set.aggregate(total=Sum('total_payment'))
    return summ['total']

@register.filter()
def summ_profits(query_set):
    summ = query_set.aggregate(total=Sum('gross_profit'))
    return summ['total']

@register.filter()
def summ_payment_amount(query_set):
    summ = 0
    for item in query_set:
        if item.category.name == 'expense':
            summ -= item.amount
        else:
            summ += item.amount
    return summ
