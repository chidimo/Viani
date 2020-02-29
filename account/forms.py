from django import forms
from django.urls import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper

from .models import Revenue, ExpenditureType, Expenditure

class NewRevenue(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = ('date', 'amount', 'notes')

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes', 'rows': 3}),
        }

class AddRevenueToJobForm(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = ('date', 'amount', 'notes')

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes', 'rows': 3}),
        }


class NewExpenditureTypeForm(forms.ModelForm):
    class Meta:
        model = ExpenditureType
        fields = ('name', 'description')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class NewExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ('date', 'amount', 'item', 'category', 'notes')

        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control',}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': AddAnotherWidgetWrapper(
                forms.Select(attrs={'class': 'form-control'}),
                reverse_lazy('account:new_expenditure_type')),
        }


class AddExpenditureToJobForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ('date', 'item', 'amount', 'notes')

        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control',}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
