from django import forms
from django.urls import reverse_lazy

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
        fields = ('customer', 'short_description', 'value', 'discount', 'notes')

        widgets = {
            'customer' : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('shop:customer_new')
            ),
            'short_description' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Describe job in 30 characters'}),
            'value' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter job price'}),
            'discount' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter discount (if any)'}),
            'notes' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Any notes or longer description'}),
        }

class EditJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('customer', 'short_description', 'value', 'discount', 'notes')

        widgets = {
            'customer' : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy('shop:customer_new')
            ),
            'short_description' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Describe job in 30 characters'}),
            'value' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter job price'}),
            'discount' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter discount (if any)'}),
            'notes' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Any notes or longer description'}),
        }

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

class UpdateJobStatusForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('status', 'notes')

        widgets = {
            'status' : forms.Select(attrs={'class' : 'form-control'}),
            'notes' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Notes'}),
        }
