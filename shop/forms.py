from django import forms

from .models import Job, JobExpense, JobPayment

class NewJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('customer', 'value', 'discount',)

        widgets = {
            'customer' : forms.Select(attrs={'class' : 'form-control'}),
            'value' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'discount' : forms.NumberInput(attrs={'class' : 'form-control'}),
        }
