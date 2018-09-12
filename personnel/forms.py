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

from bet9ja.models import Product

from .models import Personnel, PersonnelPermission, Designation
from universal.utils import get_model_list

Person = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter username'}))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter password'}))

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

class NewDesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ('designation',  'description')
        widgets = {
            "designation" : forms.TextInput(
                attrs={'class':'form-control', 'placeholder' : 'Enter designation'}),

            "description" : forms.Textarea(
                attrs={'class':'form-control', 'placeholder' : 'Description'}),
            }

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
        fields = ("first_name", "last_name", "address", "phone", "bank", "avatar")

        widgets = {

            "first_name" : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'First name'}),

            "last_name" : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Last name'}),

            "address" : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Address'}),

            "bank" : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy("service:new")),

            "phone" : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Phone'}),

            'avatar' : ClearableFileInput(attrs={'class' : 'form-control'})
            }

class PersonnelAvatarAddForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ("avatar",)
        widgets = {
            'avatar' : ClearableFileInput(attrs={'class' : 'form-control'})
            }

class PersonnelEditByManagerForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ("status", "designation", "bank", "salary")

        widgets = {

            "status" : forms.Select(attrs={'class' : 'form-control'}),

            "designation" : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy("personnel:new_designation")),

            "bank" : AddAnotherWidgetWrapper(
                forms.Select(attrs={'class' : 'form-control'}),
                reverse_lazy("service:new")),

            "salary" : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Base pay'}),
            }

class SelectDateRangeForm(forms.Form):
    from_date = DateField(
        initial=timezone.now,
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}))
    to_date = DateField(
        initial=timezone.now() + datetime.timedelta(days=7),
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}))

# class NewPermissionForm(forms.Form):
#     name = forms.CharField(widget=forms.TextInput(
#         attrs={'class' : 'form-control', 'placeholder' : 'Permission name'}))
#     codename = forms.CharField(required=False, widget=forms.TextInput(
#         attrs={'class' : 'form-control', 'placeholder' : 'Permission Code name - Optional'}))
#     app_name_model_name = forms.ChoiceField(choices=get_model_list(),
#         widget=forms.Select(attrs={"class" : "form-control"}))

class NewGroupForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class' : 'form-control', 'placeholder' : 'Group name'}))

class AddPersonnelToGroupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        group_name = kwargs.pop('group_name', None)
        super(AddPersonnelToGroupForm, self).__init__(*args, **kwargs)
        self.fields['personnels'].queryset = Personnel.objects.exclude(user__groups__name__in=[group_name])

    personnels = forms.ModelMultipleChoiceField(
        queryset=Personnel.objects.all(),
        widget=forms.CheckboxSelectMultiple())

class RemovePersonnelFromGroupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        group_name = kwargs.pop('group_name', None)
        super(RemovePersonnelFromGroupForm, self).__init__(*args, **kwargs)
        self.fields['personnels'].queryset = Personnel.objects.filter(user__groups__name__in=[group_name])

    personnels = forms.ModelMultipleChoiceField(
        queryset=Personnel.objects.all(),
        widget=forms.CheckboxSelectMultiple())

class GrantPersonnelPermissionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        permission = kwargs.pop("permission")
        super(GrantPersonnelPermissionForm, self).__init__(*args, **kwargs)
        self.fields['personnels'].queryset = Personnel.objects.exclude(
            personnelpermission__name=permission.name
            )
    personnels = forms.ModelMultipleChoiceField(
        queryset=Personnel.objects.all(),
        widget=forms.CheckboxSelectMultiple())

class RevokePersonnelPermissionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        permission = kwargs.pop("permission")
        super(RevokePersonnelPermissionForm, self).__init__(*args, **kwargs)
        self.fields['personnels'].queryset = Personnel.objects.filter(
            personnelpermission__name=permission.name
            )
    personnels = forms.ModelMultipleChoiceField(
        queryset=Personnel.objects.all(),
        widget=forms.CheckboxSelectMultiple())

custom_error_messages = {
    'required': 'You must select at least one item from this list.',
}

class GrantMultiplePermissionsForm(forms.Form):
    permissions = forms.ModelMultipleChoiceField(
        required=True,
        queryset=PersonnelPermission.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        error_messages=custom_error_messages,
        )
    personnels = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Personnel.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        error_messages=custom_error_messages,
        )

class PersonnelSaleFilterForm(forms.Form):
    product = forms.ModelChoiceField(
        required=False,
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={"class" : "form-control"}))
    from_date = DateField(
        required=True,
        initial=timezone.now,
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}))

    to_date = DateField(
        required=True,
        initial=timezone.now() + datetime.timedelta(days=7),
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'class' : 'form-control'}))
