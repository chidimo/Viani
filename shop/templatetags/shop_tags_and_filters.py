from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def status_text(value):
    return {1: 'Started', 2: "Finished", 3: 'Delivered', 4: 'Accepted'}[value]

@register.filter()
def summ_values(query_set):
    return query_set.aggregate(total=Sum('value'))['total']

@register.filter()
def summ_discounts(query_set):
    return query_set.aggregate(total=Sum('discount'))['total']

@register.filter()
def summ_total_expenses(query_set):
    exp = 0
    for item in query_set:
        expenses = item.expenditure_set.aggregate(total=Sum('amount'))['total']
        exp += expenses if expenses else 0
    return exp

@register.filter()
def summ_total_payments(query_set):
    pay = 0
    for item in query_set:
        rev = item.revenue_set.aggregate(total=Sum('amount'))['total']
        pay += rev if rev else 0
    return pay

@register.filter()
def summ_profits(query_set):
    profit = 0
    for item in query_set:
        rev = item.revenue_set.aggregate(total=Sum('amount'))['total']
        expenses = item.expenditure_set.aggregate(total=Sum('amount'))['total']
        profit += rev if rev else 0
        profit -= expenses if expenses else 0
    return profit

    return query_set.aggregate(total=Sum('gross_profit'))['total']

@register.filter()
def sum_amounts(query_set):
    total = query_set.aggregate(total=Sum('amount'))['total']
    return total if total else 0

@register.filter()
def get_job_profit(job):
    profit = 0
    pay = job.revenue_set.aggregate(total=Sum('amount'))['total']
    exp = job.expenditure_set.aggregate(total=Sum('amount'))['total']
    profit += pay if pay else 0
    profit -= exp if exp else 0
    return profit
