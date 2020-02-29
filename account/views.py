from django.views import generic
from django.db.models import Q, Sum
from pure_pagination.mixins import PaginationMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Revenue, Expenditure

class ExpenditureIndex(LoginRequiredMixin, PaginationMixin, generic.ListView):
    model = Expenditure
    template_name = 'account/expenditures.html'
    context_object_name = "expenditures"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(ExpenditureIndex, self).get_context_data(**kwargs)
        # context['month_balance_form'] = NewMonthBalanceForm
        # context['expenditure_filter_form'] = ExpenditureFilterForm
        context['total_expenditure_value'] = Expenditure.objects.aggregate(
            total=Sum('amount'))['total']
        return context

    def get_queryset(self):
        return Expenditure.objects.all()


class RevenueIndex(LoginRequiredMixin, PaginationMixin, generic.ListView):
    model = Revenue
    template_name = 'account/revenues.html'
    context_object_name = 'revenues'
    paginate_by = 100

    def get_queryset(self):
        return Revenue.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(RevenueIndex, self).get_context_data(*args, **kwargs)

        # context['rev_filter_form'] = RevenueFilterForm()
        context['total_revenue_value'] = Revenue.objects.aggregate(total=Sum('amount'))[
            'total']
        return context
