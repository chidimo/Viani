from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin

import rules
from .utils import context_messages as cm

from .models import Customer, Job, CashFlow, CashFlowType
from .forms import NewCustomerForm, NewJobForm, NewCashFlowForm, AddCashFlowToJobForm, NewCashFlowTypeForm

def gallery(request):
    template = 'shop/gallery.html'
    context = {}
    return render(request, template, context)

class CustomerIndex(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = 'shop/customer_index.html'
    context_object_name = 'customers'
    paginate_by = 100

class NewCustomer(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Customer
    template_name = 'shop/customer_new.html'
    form_class = NewCustomerForm
    success_message = 'Customer added successfully !'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if rules.test_rule('create_customer', user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(self.request, cm.OPERATION_FAILED)
        return redirect('/')

class JobIndex(LoginRequiredMixin, generic.ListView):
    model = Job
    template_name = 'shop/job_index.html'
    context_object_name = 'jobs'
    paginate_by = 100

class NewJob(CreatePopupMixin, LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Job
    form_class = NewJobForm
    template_name = 'shop/job_new.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if rules.test_rule('create_job', user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(self.request, cm.OPERATION_FAILED)
        return redirect('/')

class JobDetail(LoginRequiredMixin, generic.DetailView):
    model = Job
    template_name = 'shop/job_detail.html'
    context_object_name = 'job'

def job_add_cashflow(request, pk):
    job = Job.objects.get(pk=pk)
    template = 'shop/job_add_cashflow.html'
    form = AddCashFlowToJobForm()

    context = {}
    context['form'] = form
    context['job'] = job

    if request.method == 'POST':
        form = AddCashFlowToJobForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            category = form['category']
            name = form['name']
            amount = form['amount']
            notes = form['notes']
            cashflow = CashFlow.objects.create(category=category, name=name, amount=amount, job=job, notes=notes)
            return redirect(cashflow.get_absolute_url())
        else:
            return render(request, template, {'form' : form})

    return render(request, template, context)

class CashFlowTypeIndex(LoginRequiredMixin, generic.ListView):
    model = CashFlowType
    template_name = 'shop/cashflowtype_index.html'
    context_object_name = 'cashflowtypes'
    paginate_by = 100

class NewCashFlowType(LoginRequiredMixin, generic.CreateView):
    model = CashFlowType
    form_class = NewCashFlowTypeForm
    template_name = 'shop/cashflowtype_new.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if rules.test_rule('create_cashflowtype', user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(self.request, cm.OPERATION_FAILED)
        return redirect('/')

class CashFlowIndex(LoginRequiredMixin, generic.ListView):
    model = CashFlow
    template_name = 'shop/cashflow_index.html'
    context_object_name = 'cashflows'
    paginate_by = 100

class NewCashFlow(LoginRequiredMixin, generic.CreateView):
    model = CashFlow
    form_class = NewCashFlowForm
    template_name = 'shop/cashflow_new.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if rules.test_rule('create_cashflow', user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(self.request, cm.OPERATION_FAILED)
        return redirect('/')

def bank_cashflow(request, pk):

    if rules.test_rule('bank_cashflow', request.user) is False:
        messages.error(request, cm.OPERATION_FAILED)
    
    cashflow = CashFlow.objects.get(pk=pk)

    if cashflow.category.name == 'expense':
        messages.error(request, 'You cannot bank an expense')
    else:
        cashflow.banked = True
        cashflow.save(update_fields=['banked'])

    return redirect('shop:cashflow_index')
