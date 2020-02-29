from django.views import generic
from django.db.models import Q, Sum
from django.contrib import messages
from pure_pagination.mixins import PaginationMixin
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from django_addanother.views import CreatePopupMixin

from shop.models import Job
from constants.banner import BANNER
from v_rules.PermissionBackend import vianirules
# from personnel.models import Personnel
from .models import Revenue, ExpenditureType, Expenditure
from .forms import AddRevenueToJobForm, AddExpenditureToJobForm, NewExpenditureForm, NewExpenditureTypeForm


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


class NewExpenditure(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    model = Expenditure
    form_class = NewExpenditureForm
    template_name = "account/expenditure_new.html"

    def dispatch(self, request, *args, **kwargs):
        rule_to_check = 'create_expenditure'
        if vianirules.has_permission(rule_to_check, self.request):
            return super().dispatch(*args, request, **kwargs)
        messages.error(self.request, BANNER['INSUFFICIENT_RIGHT'])
        return redirect('account:expenditures')

@login_required
def add_expenditure_to_job(request, pk):
    job = Job.objects.get(pk=pk)
    template = 'account/expenditure_add_to_job.html'

    # if job.status == 4:
    #     messages.error(request, "This job can no longer accept a revenue.")
    #     return redirect(reverse('shop:job_detail', kwargs={'pk': job.pk}))

    context = {}
    context['job'] = job
    context['form'] = AddExpenditureToJobForm()

    if request.method == 'POST':
        form = AddExpenditureToJobForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data

            date = form['date']
            notes = form['notes']
            amount = form['amount']

            Expenditure.objects.create(
                date=date, personnel=request.user.personnel, amount=amount, job=job, notes=notes)
            return redirect(reverse('shop:job_detail', kwargs={'pk': pk}))
        else:
            return render(request, template, {'form': form})
    return render(request, template, context)


class NewExpenditureType(LoginRequiredMixin, CreatePopupMixin, generic.CreateView):
    model = ExpenditureType
    form_class = NewExpenditureTypeForm
    template_name = "account/expenditure_type_new.html"

    def dispatch(self, request, *args, **kwargs):
        if vianirules.has_permission('create_expendituretype', self.request):
            return super().dispatch(*args, request, **kwargs)
        messages.error(self.request, BANNER['INSUFFICIENT_RIGHT'])
        return redirect('account:expenditures')

    def form_valid(self, form):
        messages.success(self.request, BANNER['SUCCESS'])
        return super(NewExpenditureType, self).form_valid(form)

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


@login_required
def add_revenue_to_job(request, pk):
    job = Job.objects.get(pk=pk)
    template = 'account/revenue_add_to_job.html'

    # if job.status == 4:
    #     messages.error(request, "This job can no longer accept a revenue.")
    #     return redirect(reverse('shop:job_detail', kwargs={'pk': job.pk}))

    context = {}
    context['job'] = job
    context['form'] = AddRevenueToJobForm()

    if request.method == 'POST':
        form = AddRevenueToJobForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data

            date = form['date']
            notes = form['notes']
            amount = form['amount']

            Revenue.objects.create(
                date=date, personnel=request.user.personnel, amount=amount, job=job, notes=notes)
            return redirect(reverse('shop:job_detail', kwargs={'pk': pk}))
        else:
            return render(request, template, {'form': form})
    return render(request, template, context)


def accounting(request):
    template = 'account/accounting.html'
    context = {}

    total_job_value = Job.objects.aggregate(total=Sum('value'))['total']
    total_discounts = Job.objects.aggregate(total=Sum('discount'))['total']
    total_payments = Revenue.objects.aggregate(total=Sum('amount'))['total']
    total_expenses = Expenditure.objects.aggregate(total=Sum('amount'))['total']

    net_profit = total_payments - total_expenses

    context['net_profit'] = net_profit
    context['total_payments'] = total_payments
    context['total_expenses'] = total_expenses
    context['total_job_value'] = total_job_value
    context['total_discounts'] = total_discounts

    return render(request, template, context)
