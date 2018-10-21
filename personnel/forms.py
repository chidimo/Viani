"""forms"""

import datetime

from django import forms
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.forms.widgets import ClearableFileInput
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group, Permission

from django.forms.fields import DateField

from django_addanother.widgets import AddAnotherWidgetWrapper

from .models import Personnel, PersonnelPermission, Designation

Person = get_user_model()

class PersonCreationForm(forms.ModelForm):
    """Custom UCF. Takes the standard
    variables of 'email', 'password1', 'password2'
    For creating instances of 'Person'."""
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Re-enter Password", widget=forms.PasswordInput)

    class Meta:
        model = Person
        fields = ('email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        Person = super(PersonCreationForm, self).save(commit=False)
        Person.set_password(self.cleaned_data["password1"])
        if commit:
            Person.save()
        return Person

class PersonChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = Person
        fields = ("email", "password", "is_active", "is_admin")

    def clean_password(self):
        return self.initial["password"]

class PersonnelMixin(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ("display_name", "first_name", "last_name")

        widgets = {
            "display_name" : forms.TextInput(
                attrs={'class':'form-control', 'placeholder' : 'Choose a display name'}),

            "first_name" : forms.TextInput(
                attrs={'class':'form-control', 'placeholder' : 'First name'}),

            "last_name" : forms.TextInput(
                attrs={'class':'form-control', 'placeholder' : 'Last name'}),
        }

        def clean_display_name(self):
            display_name = self.cleaned_data["display_name"]
            if Personnel.objects.filter(display_name=display_name).exists():
                raise forms.ValidationError("Display name already taken.")
            return display_name

class PersonnelRegistrationForm(forms.Form):
    # Person creation data
    email_address = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Email address (required)'})
        )

    display_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Display name (required)'})
    )

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'First name (required)'})
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Last name (required)'})
    )

    def clean_email(self):
        email_address = self.cleaned_data["email_address"]
        if Person.objects.filter(email=email_address).exists():
            raise forms.ValidationError("Email already exists.")
        return email_address

class PersonnelEditForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ("first_name", "last_name", "address", "phone", "avatar")

        widgets = {

            "first_name" : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'First name'}),

            "last_name" : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Last name'}),

            "address" : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Address'}),

            "phone" : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Phone'}),

            'avatar' : ClearableFileInput(attrs={'class' : 'form-control'})
            }
