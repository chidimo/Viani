"""Docstring"""
import operator
from functools import reduce
from datetime import timedelta

from django.db import IntegrityError
from django.db.models import Q
from django.views import generic
from django.conf import settings
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required#, user_passes_test
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator

import rules

from pure_pagination import PaginationMixin
from django_addanother.views import CreatePopupMixin

from .utils.view_decorators import personnel_is_ceo, personnel_is_ceo_or_manager, personnel_belongs_to_it, personnel_is_self_ceo_or_manager
from .utils import context_messages as cm

from .utils.utils import check_recaptcha
from .models import Personnel, PersonnelPermission, Designation
from .forms import (
    PersonnelRegistrationForm, PersonnelEditForm
)

Person = get_user_model()

class PersonnelIndex(PaginationMixin, LoginRequiredMixin, generic.ListView):
    model = Personnel
    context_object_name = 'personnels'
    template_name = "personnel/index.html"
    paginate_by = 25

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if rules.test_rule('view_personnel_index', user):
            return super().dispatch(*args, **kwargs)
        messages.error(self.request, cm.RESTRICTED_PAGE)
        return redirect('/')
