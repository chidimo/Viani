import datetime

from django import forms
from django.utils import timezone
from django.urls import reverse_lazy
from django.forms.fields import DateField

from .models import Customer, Job, CashFlow, CashFlowType

from django_addanother.widgets import AddAnotherWidgetWrapper

class NewCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'phone', 'address', 'sex')

        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' :'Enter first name'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' :'Enter last name'}),
            'address' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' :'Enter address name'}),
            'phone' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' :'Enter phone number'}),
            'sex' : forms.Select(attrs={'class' : 'form-control'}),
        }

class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'phone', 'address', 'sex')

        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' :'Enter first name'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' :'Enter last name'}),
            'address' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' :'Enter address name'}),
            'phone' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' :'Enter phone number'}),
            'sex' : forms.Select(attrs={'class' : 'form-control'}),
        }

class NewJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('start_date', 'customer', 'short_description', 'value', 'discount', 'notes')

        widgets = {
            'customer' : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('shop:customer_new')
            ),
            'start_date' : forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}),
            'short_description' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Describe job in 30 characters'}),
            'value' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter job price'}),
            'discount' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter discount (if any)'}),
            'notes' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Any notes or longer description'}),
        }

class EditJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('start_date', 'customer', 'short_description', 'value', 'discount', 'notes')

        widgets = {
            'customer' : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('shop:customer_new')
            ),
            'start_date' : forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}),
            'short_description' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Describe job in 30 characters'}),
            'value' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter job price'}),
            'discount' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter discount (if any)'}),
            'notes' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Any notes or longer description'}),
        }

class UpdateJobStatusForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('status', 'completed', 'notes')

        widgets = {
            'completed' : forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}),
            'status' : forms.Select(attrs={'class' : 'form-control'}),
            'notes' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Notes'}),
        }

class JobFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].label = 'Job start date'
        self.fields['completed'].label = 'Job completion date'
        self.fields['to_date'].label = 'Find to date'

    phase = forms.ChoiceField(
        required=False,
        choices = (('', 'Select phase'), (1, 'Phase 1'), (2, 'Phase 2'), (3, 'Phase 3'), (4, 'Phase 4'), (5, 'Phase 5')),
        widget=forms.Select(attrs={"class" : "form-control"})
        )
    customer = forms.ModelChoiceField(
        required=False,
        empty_label = 'Select customer',
        queryset=Customer.objects.all(),
        widget=forms.Select(attrs={"class" : "form-control"}))

    start_date = DateField(
        required=False,
        # initial=timezone.now,
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}))

    completed= DateField(
        required=False,
        # initial=timezone.now,
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}))

    to_date = DateField(
        required=True,
        initial=timezone.now() + datetime.timedelta(days=30),
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}))

class NewCashFlowTypeForm(forms.ModelForm):
    class Meta:
        model = CashFlowType
        fields = ('name', 'description',)

        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control' ,'placeholder' : 'Enter cashflowtype name'}),
            'description' : forms.Textarea(attrs={'class' : 'form-control' ,'placeholder' : 'Enter cashflowtype description'}),
        }

class NewCashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = ('job', 'category', 'name', 'amount', 'notes')

        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter name of item (if applicable)'}),
            'category' : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('shop:cashflowtype_new')
            ),
            'job' : forms.Select(attrs={'class' : 'form-control'}),
            'amount' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter amount'}),
            'notes' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Notes'}),
        }

class AddCashFlowToJobForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = ('category', 'amount', 'name', 'notes')

        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter name of item (if applicable)'}),
            'category' : forms.Select(attrs={'class' : 'form-control'}),
            'amount' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter amount'}),
            'notes' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Notes'}),
        }

class CashFlowFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_date'].label = 'Payment date'

    job = forms.ModelChoiceField(
        required=False,
        empty_label = 'Select job',
        queryset=Job.objects.all(),
        widget=forms.Select(attrs={"class" : "form-control"}))

    customer = forms.ModelChoiceField(
        required=False,
        empty_label = 'Select customer',
        queryset=Customer.objects.all(),
        widget=forms.Select(attrs={"class" : "form-control"}))

    category = forms.ModelChoiceField(
        required=False,
        empty_label = 'Select cashflowype',
        queryset=CashFlowType.objects.all(),
        widget=forms.Select(attrs={"class" : "form-control"}))

    payment_date = DateField(
        required=False,
        initial=timezone.now,
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}))

    to_date = DateField(
        required=True,
        initial=timezone.now() + datetime.timedelta(days=30),
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}))
