import datetime
import operator
from functools import reduce

from django.views import generic
from django.db.models import Q, Sum
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django_addanother.views import CreatePopupMixin
from pure_pagination.mixins import PaginationMixin

from account.models import Revenue, Expenditure

from .utils import context_messages as cm

from .models import Customer, Job
from .forms import (
    NewCustomerForm, EditCustomerForm, NewJobForm, EditJobForm,
    UpdateJobStatusForm, JobFilterForm
)

from v_rules.PermissionBackend import vianirules


class CustomerIndex(LoginRequiredMixin, PaginationMixin,  generic.ListView):
    model = Customer
    template_name = 'shop/customer_index.html'
    context_object_name = 'customers'
    paginate_by = 100

    def get_queryset(self):
        return super().get_queryset()


class NewCustomer(CreatePopupMixin, LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Customer
    template_name = 'shop/customer_new.html'
    form_class = NewCustomerForm
    success_message = 'Customer added successfully !'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        rule_to_check = 'create_customer'
        if vianirules.has_permission(rule_to_check, request):
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
        rule_to_check = 'edit_customer'

        if vianirules.has_permission(rule_to_check, request):
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
    paginate_by = 2

    def dispatch(self, request, *args, **kwargs):
        rule_to_check = 'view_jobs_index'
        if vianirules.has_permission(rule_to_check, self.request):
            return super().dispatch(request, *args, **kwargs)
        messages.error(self.request, cm.OPERATION_FAILED)
        return redirect('/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        completed_job_count = Job.objects.filter(status=4).count()
        total_job_count = Job.objects.count()

        context['completed_job_count'] = completed_job_count
        context['total_job_count'] = total_job_count
        try:
            completion_rate = (completed_job_count / total_job_count) * 100
        except ZeroDivisionError:
            completion_rate = 1
        context['completion_rate'] = round(completion_rate, 2)
        context['job_filter_form'] = JobFilterForm()
        context['filter_view'] = False

        overall_value = Job.objects.aggregate(total=Sum('value'))['total']
        context['overall_value'] = overall_value

        overall_discount = Job.objects.aggregate(
            total=Sum('discount'))['total']
        context['overall_discount'] = overall_discount

        overall_payment = Revenue.objects.aggregate(
            total=Sum('amount'))['total']
        context['overall_payment'] = overall_payment

        overall_job_expenditure = Expenditure.objects.filter(category__name__in=[
                                                             'materials', 'external job']).aggregate(total=Sum('amount'))['total']
        context['overall_job_expenditure'] = overall_job_expenditure

        overall_profit = 0
        overall_profit += overall_payment if overall_payment else 0
        overall_profit -= overall_job_expenditure if overall_job_expenditure else 0
        context['overall_profit'] = overall_profit
        return context


class NewJob(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Job
    form_class = NewJobForm
    template_name = 'shop/job_new.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        rule_to_check = 'create_job'
        if vianirules.has_permission(rule_to_check, request):
            return super().dispatch(request, *args, **kwargs)
        messages.error(self.request, cm.OPERATION_FAILED)
        return redirect('/')


class EditJob(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Job
    form_class = EditJobForm
    template_name = 'shop/job_edit.html'

    def get_success_url(self, **kwargs):
        return reverse('shop:job_detail', kwargs={'pk': self.kwargs['pk']})

    # def dispatch(self, request, *args, **kwargs):
    #     user = self.request.user
    #     rule_to_check = 'edit_job'
    #     if vianirules.has_permission(rule_to_check, request):
    #         return super().dispatch(request, *args, **kwargs)
    #     messages.error(self.request, cm.OPERATION_FAILED)
    #     return redirect(reverse('shop:job_detail', kwargs={'pk': self.kwargs['pk']}))


def mark_accepted(request, pk):
    user = request.user

    rule_to_check = 'mark_accepted'
    if vianirules.has_permission(rule_to_check, request):
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
                phases = {1: 'Started', 2: "Finished",
                          3: 'Delivered', 4: 'Accepted'}
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
                    messages.success(
                        self.request, "You did not make any selection")
                    return Job.objects.all().order_by('status', 'customer', '-start_date')

                # execute query
                messages.success(
                    self.request, "Search results for {}".format(query_str))
                return Job.objects.filter(query).order_by('status', 'customer', '-start_date')
