import datetime
import operator
from functools import reduce

from django.db.models import Q, Sum
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
from .forms import (
    NewCustomerForm, EditCustomerForm, NewJobForm, EditJobForm,
    UpdateJobStatusForm, JobFilterForm, NewCashFlowForm,
    NewCashFlowTypeForm, AddCashFlowToJobForm, CashFlowFilterForm
)

class CustomerIndex(LoginRequiredMixin, PaginationMixin,  generic.ListView):
    model = Customer
    template_name = 'shop/customer_index.html'
    context_object_name = 'customers'
    paginate_by = 100

class NewCustomer(CreatePopupMixin, LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
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

    def get_success_url(self, **kwargs):
        return reverse('shop:customer_details', kwargs={'pk': self.kwargs['pk']})

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
        completed_job_count = Job.objects.filter(status=4).count()
        total_job_count = Job.objects.count()
        context['completed_job_count'] = completed_job_count
        context['total_job_count'] = total_job_count
        completion_rate = (completed_job_count / total_job_count) * 100
        context['completion_rate'] = round(completion_rate, 2)
        context['job_filter_form'] = JobFilterForm()
        context['filter_view'] = False
        return context

class NewJob(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
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

    def get_success_url(self, **kwargs):
        return reverse('shop:job_detail', kwargs={'pk': self.kwargs['pk']})

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if rules.test_rule('edit_job', user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(self.request, cm.OPERATION_FAILED)
        return redirect(reverse('shop:job_detail', kwargs={'pk': self.kwargs['pk']}))

def mark_accepted(request, pk):
    user = request.user
    if rules.test_rule('mark_accepted', user):
        job = Job.objects.get(pk=pk)
        job.status = 4
        job.save()
        return redirect(reverse('shop:job_detail', kwargs={'pk': pk}))
    messages.error(request, cm.OPERATION_FAILED)
    return redirect(reverse('shop:job_detail', kwargs={'pk': pk}))

class JobDetail(LoginRequiredMixin, generic.DetailView):
    model = Job
    template_name = 'shop/job_detail.html'
    context_object_name = 'job'

def job_add_cashflow(request, pk):
    job = Job.objects.get(pk=pk)
    template = 'shop/job_add_cashflow.html'
    form = AddCashFlowToJobForm()

    if job.status == 4:
        messages.error(request, "This job can no longer accept a cashflow")
        return redirect(reverse('shop:job_detail', kwargs={'pk': job.pk}))

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
            return redirect(reverse('shop:job_detail', kwargs={'pk': job.pk}))
        else:
            return render(request, template, {'form' : form})
    return render(request, template, context)

class UpdateJobStatus(LoginRequiredMixin, SuccessMessageMixin,  generic.UpdateView):
    model = Job
    template_name = 'shop/job_update_status.html'
    form_class = UpdateJobStatusForm
    success_message = "Job status updated successfully."

    def get_success_url(self, **kwargs):
        return reverse('shop:job_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(pk=self.kwargs['pk'])
        return context

class JobFilterView(LoginRequiredMixin, PaginationMixin, generic.ListView):
    model = Job
    template_name = 'shop/job_index.html'
    context_object_name = "jobs"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(JobFilterView, self).get_context_data(**kwargs)
        context['job_filter_form'] = JobFilterForm()
        context['filter_view'] = True
        return context

    def get_queryset(self):
        if self.request.method == 'GET':
            form = JobFilterForm(self.request.GET)

            if form.is_valid():
                form = form.cleaned_data

                customer = form['customer']
                phase = form['phase']
                start_date = form['start_date']
                completed = form['completed']
                to_date = form['to_date']

                # build queries
                phases = {1: 'Started', 2: "Finished", 3: 'Delivered', 4: 'Accepted'}
                queries = []
                msg = []
                if customer:
                    queries.append(Q(customer=customer))
                    msg.append(f'{customer}')
                if phase:
                    queries.append(Q(status=phase))
                    msg.append(f'{phases[int(phase)]} jobs')

                if completed:
                    if not to_date:
                        to_date = start_date + datetime.timedelta(days=30)
                    queries.append(Q(start_date__range=[start_date, to_date]))
                    msg.append(f'Completed between {start_date} and {to_date}')

                if start_date:
                    if not to_date:
                        to_date = start_date + datetime.timedelta(days=30)
                    queries.append(Q(start_date__range=[start_date, to_date]))
                    msg.append(f'Started between {start_date} and {to_date}')

                # combine queries
                try:
                    query = reduce(operator.and_, queries)
                    query_str = " AND ".join(msg)
                except TypeError:
                    query = []
                    query_str = ""
                    messages.success(self.request, "You did not make any selection")
                    return Job.objects.all().order_by('status', 'customer', '-start_date')

                # execute query
                messages.success(self.request, "Search results for {}".format(query_str))
                return Job.objects.filter(query).order_by('status', 'customer', '-start_date')

class CashFlowTypeIndex(LoginRequiredMixin, PaginationMixin, generic.ListView):
    model = CashFlowType
    template_name = 'shop/cashflowtype_index.html'
    context_object_name = 'cashflowtypes'
    paginate_by = 100

class NewCashFlowType(CreatePopupMixin, LoginRequiredMixin, generic.CreateView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cashflow_filter_form'] = CashFlowFilterForm()
        return context

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

class CashFlowFilterView(LoginRequiredMixin, PaginationMixin, generic.ListView):
    model = CashFlow
    template_name = 'shop/cashflow_index.html'
    context_object_name = "cashflows"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(CashFlowFilterView, self).get_context_data(**kwargs)
        context['cashflow_filter_form'] = CashFlowFilterForm()
        return context

    def get_queryset(self):
        if self.request.method == 'GET':
            form = CashFlowFilterForm(self.request.GET)

            if form.is_valid():
                form = form.cleaned_data

                customer = form['customer']
                job = form['job']
                category = form['category']
                start_date = form['start_date']
                to_date = form['to_date']

                # build queries
                queries = []
                msg = []
                if job:
                    queries.append(Q(job=job))
                    msg.append(f'{job}')
                if customer:
                    queries.append(Q(job__customer=customer))
                    msg.append(f'{customer}')
                if category:
                    queries.append(Q(category=category))
                    msg.append(f'{category}')

                if start_date:
                    if not to_date:
                        to_date = start_date + datetime.timedelta(days=30)
                    queries.append(Q(created__range=[start_date, to_date]))
                    msg.append(f'Paid between {start_date} and {to_date}')

                # combine queries
                try:
                    query = reduce(operator.and_, queries)
                    query_str = " AND ".join(msg)
                except TypeError:
                    query = []
                    query_str = ""

                # execute query
                messages.success(self.request, f"Search results for {query_str}")
                return CashFlow.objects.filter(query).order_by('job', 'category', 'banked')

def accounting(request):
    template = 'shop/accounting.html'
    context = {}

    context['total_job_value'] = Job.objects.aggregate(total=Sum('value'))['total']
    context['total_payments'] = Job.objects.aggregate(total=Sum('total_payment'))['total']
    context['total_expenses'] = CashFlow.objects.filter(category__name='expense').aggregate(total=Sum('amount'))['total']
    context['total_discounts'] = Job.objects.aggregate(total=Sum('discount'))['total']
    context['gross_profit'] = Job.objects.aggregate(total=Sum('gross_profit'))['total']
    context['total_amount_banked'] = CashFlow.objects.filter(banked=True, category__name='payment').aggregate(total=Sum('amount'))['total']
    context['net_profit'] = 'Deduct overheads'

    return render(request, template, context)
