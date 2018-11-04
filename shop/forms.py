from django import forms
from django.urls import reverse_lazy

from .models import Customer, Job, CashFlow, CashFlowType

from django_addanother.widgets import AddAnotherWidgetWrapper

class NewCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'phone', 'address', 'sex')

        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'address' : forms.TextInput(attrs={'class' : 'form-control'}),
            'phone' : forms.TextInput(attrs={'class' : 'form-control'}),
            'sex' : forms.Select(attrs={'class' : 'form-control'}),
        }

class NewJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('customer', 'value', 'discount',)

        widgets = {
            'customer' : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('shop:customer_new')
            ),
            'value' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'discount' : forms.NumberInput(attrs={'class' : 'form-control'}),
        }

class NewCashFlowTypeForm(forms.ModelForm):
    class Meta:
        model = CashFlowType
        fields = ('name', 'description',)

        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'description' : forms.Textarea(attrs={'class' : 'form-control'}),
        }

class NewCashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = ('job', 'category', 'name', 'amount', 'notes')

        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'category' : forms.Select(attrs={'class' : 'form-control'}),
            'job' : forms.Select(attrs={'class' : 'form-control'}),
            'amount' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'notes' : forms.Textarea(attrs={'class' : 'form-control'}),
        }
