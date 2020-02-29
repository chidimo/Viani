import datetime

from django import forms
from django.utils import timezone
from django.urls import reverse_lazy
from django.forms.fields import DateField

from .models import Customer, Job

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
        fields = ('start_date', 'customer', 'description', 'value', 'discount', 'notes')

        widgets = {
            'customer' : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('shop:customer_new')
            ),
            'start_date' : forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}),
            'description' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Describe job in 30 characters'}),
            'value' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter job price'}),
            'discount' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter discount (if any)'}),
            'notes' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Any notes or longer description'}),
        }

class EditJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('start_date', 'customer', 'description', 'value', 'discount', 'notes')

        widgets = {
            'customer' : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('shop:customer_new')
            ),
            'start_date' : forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}),
            'description' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Describe job in 30 characters'}),
            'value' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter job price'}),
            'discount' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter discount (if any)'}),
            'notes' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Any notes or longer description'}),
        }

class UpdateJobStatusForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('status',)

        widgets = {
            'status' : forms.Select(attrs={'class' : 'form-control'}),
        }

class JobFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].label = 'Job start date'
        self.fields['completed'].label = 'Job completion date'
        self.fields['to_date'].label = 'Find to date'

    phase = forms.ChoiceField(
        required=False,
        choices = ((1, 'Started'), (2, "Finished"), (3,  'Delivered'), (4, 'Accepted')),
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
