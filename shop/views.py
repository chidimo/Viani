from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin

import rules
from .utils import context_messages as cm

from .models import Customer, Job, CashFlow, CashFlowType
from .forms import NewCustomerForm, EditCustomerForm, NewJobForm, EditJobForm, NewCashFlowForm, AddCashFlowToJobForm, UpdateJobStatusForm, NewCashFlowTypeForm

def gallery(request):
    template = 'shop/gallery.html'
    context = {}
    return render(request, template, context)

class CustomerIndex(LoginRequiredMixin, PaginationMixin,  generic.ListView):
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

class EditCustomer(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Customer
    template_name = 'shop/customer_edit.html'
    form_class = EditCustomerForm
    success_message = 'Customer updated successfully !'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if rules.test_rule('edit_customer', user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(self.request, cm.OPERATION_FAILED)
        return redirect('/')

def customer_details(request, pk):
    template = 'shop/customer_details.html'
    context = {}
    context['customer'] = Customer.objects.get(pk=pk)
    context['customer_jobs'] = Job.objects.filter(customer__pk=pk)
    return render(request, template, context)

class JobIndex(LoginRequiredMixin, PaginationMixin, generic.ListView):
    model = Job
    template_name = 'shop/job_index.html'
    context_object_name = 'jobs'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completed_job_count'] = Job.objects.filter(status=5).count()
        return context

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

class EditJob(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Job
    form_class = EditJobForm
    template_name = 'shop/job_edit.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if rules.test_rule('edit_job', user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(self.request, cm.OPERATION_FAILED)
        return redirect(reverse('shop:job_index'))

class JobDetail(LoginRequiredMixin, generic.DetailView):
    model = Job
    template_name = 'shop/job_detail.html'
    context_object_name = 'job'

def job_add_cashflow(request, pk):
    job = Job.objects.get(pk=pk)
    template = 'shop/job_add_cashflow.html'
    form = AddCashFlowToJobForm()

    if job.status == 'completed':
        messages.error(request, "This job is done. You can no longer add a cashflow")
        return redirect(reverse('shop:job_index'))

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
            CashFlow.objects.create(category=category, name=name, amount=amount, job=job, notes=notes)
            job.save()
            return redirect(reverse('shop:job_index'))
        else:
            return render(request, template, {'form' : form})
    return render(request, template, context)

class UpdateJobStatus(LoginRequiredMixin, SuccessMessageMixin,  generic.UpdateView):
    model = Job
    template_name = 'shop/job_update_status.html'
    form_class = UpdateJobStatusForm
    success_message = "Job status updated successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(pk=self.kwargs['pk'])
        return context

class CashFlowTypeIndex(LoginRequiredMixin, PaginationMixin, generic.ListView):
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

class CashFlowIndex(LoginRequiredMixin, PaginationMixin, generic.ListView):
    model = CashFlow
    template_name = 'shop/cashflow_index.html'
    context_object_name = 'cashflows'
    paginate_by = 100

class NewCashFlow(CreatePopupMixin, LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = CashFlow
    form_class = NewCashFlowForm
    template_name = 'shop/cashflow_new.html'
    success_message = 'Cashflow added successfully'

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
