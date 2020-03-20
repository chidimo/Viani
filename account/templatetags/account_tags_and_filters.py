from django import template
from django.db.models import Sum

from constants.month_choices import month_choices
from account.models import Expenditure

register = template.Library()


@register.filter()
def sum_expenditure_amounts_in_expenditure_queryset(query_set):
    """
    Return sum of expenditure amounts in a queryset
    """

    return query_set.aggregate(total=Sum('amount'))['total']

@register.filter()
def sum_debt_amount(queryset):
    return queryset.aggregate(total=Sum('amount'))['total']

@register.filter()
def get_month_name(value):
    return month_choices[value]

@register.filter()
def sum_aggregate_in_monthcheck_queryset(query_set):
    """
    Return sum of expenditure amounts in a queryset
    """

    return query_set.aggregate(total=Sum('aggregate_value'))['total']

@register.filter()
def get_key_from_dict(dict_object, key):
    return dict_object.get(key)

@register.filter()
def sum_revenues(revenue_qset):
    """Return sum of amounts in revenue queryset"""
    return revenue_qset.aggregate(total=Sum('amount'))['total']

@register.filter()
def get_etype_sum(category):
    """Return sum of amounts in revenue queryset"""
    return Expenditure.objects.filter(category__name=category).aggregate(total=Sum('amount'))['total']
