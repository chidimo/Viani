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
# from rules.contrib.views import PermissionRequiredMixin
# from rules.contrib.views import permission_required

from bet9ja.models import Sale, Remit
from game.models import GameRemit
from account.models import Debt, Remuneration, Expenditure
from viewcenter.models import ViewCenterRemit
from establishment.models import BranchAccessCode
from establishment.views import get_branch

from .view_decorators import personnel_is_ceo, personnel_is_ceo_or_manager, personnel_belongs_to_it, personnel_is_self_ceo_or_manager
from universal.utils import report_view
from universal import context_messages as cm

from .utils import check_recaptcha
from .models import Personnel, PersonnelPermission, Designation
from .forms import (
    LoginForm, GrantPersonnelPermissionForm, RevokePersonnelPermissionForm,
    PersonnelRegistrationForm, PersonnelEditForm, PersonnelAvatarAddForm,
    PersonnelEditByManagerForm, SelectDateRangeForm, NewGroupForm,
    AddPersonnelToGroupForm, RemovePersonnelFromGroupForm,
    NewDesignationForm, GrantMultiplePermissionsForm,
    PersonnelSaleFilterForm,
)

Person = get_user_model()

def login_view(request):
    template = 'registration/login.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                return redirect(reverse("establishment:login_user", args=[user.pk]))
            else:
                form.add_error('username', "username and password mismatch")
                return render(request, template, {'form' : form})
    else:
        form = LoginForm()
        return render(request, template, {'form' : form})

class NewDesignation(LoginRequiredMixin, SuccessMessageMixin, CreatePopupMixin, generic.CreateView):
    model = Designation
    form_class = NewDesignationForm
    template_name = 'personnel/designation_new.html'
    success_message = "Designation successfully created"

class DesignationIndex(PaginationMixin, LoginRequiredMixin, generic.ListView):
    model = Designation
    context_object_name = 'designations'
    template_name = "personnel/designations.html"
    paginate_by = 25

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

class PersonnelPermissionIndex(PaginationMixin, LoginRequiredMixin, generic.ListView):
    model = PersonnelPermission
    context_object_name = 'generic_permissions'
    template_name = "personnel/permissions_generic.html"

    def dispatch(self, *args, **kwargs):
        if rules.test_rule('view_permission_index', self.request.user):
            return super().dispatch(*args, **kwargs)
        messages.error(self.request, cm.RESTRICTED_PAGE)
        return redirect('/')

def grant_permission(request, pk):
    template = 'personnel/permission_grant.html'
    permission = PersonnelPermission.objects.get(pk=pk)
    form = GrantPersonnelPermissionForm(permission=permission)

    if rules.test_rule('permission_grant', request.user) is False:
        messages.error(request, cm.OPERATION_FAILED)
        return redirect('personnel:permissions')

    if request.method == 'POST':
        form = GrantPersonnelPermissionForm(request.POST, permission=permission)
        if form.is_valid():
            data = form.cleaned_data
            personnels = data['personnels']
            for personnel in personnels:
                permission.personnel.add(personnel)
            return redirect('personnel:permissions')
    return render(request, template, {'form' : form, 'permission' : permission})

class PersonnelPermissionDetail(LoginRequiredMixin, generic.DetailView):
    model = PersonnelPermission
    template_name = 'personnel/permission_detail.html'
    context_object_name = 'permission'

def revoke_permission(request, pk):
    permission = PersonnelPermission.objects.get(pk=pk)
    template = 'personnel/permission_revoke.html'
    form = RevokePersonnelPermissionForm(permission=permission)

    if rules.test_rule('permission_revoke', request.user) is False:
        messages.error(request, cm.OPERATION_FAILED)
        return redirect('personnel:permissions')

    if request.method == 'POST':
        form = RevokePersonnelPermissionForm(request.POST, permission=permission)
        if form.is_valid():
            data = form.cleaned_data
            personnels = data['personnels']
            for personnel in personnels:
                permission.personnel.remove(personnel)
            return redirect('personnel:permissions')
    return render(request, template, {'form' : form, 'permission' : permission})

def grant_multiple_permissions(request):
    template = 'personnel/permission_multiple.html'

    if rules.test_rule('grant_multiple_permissions', request.user) is False:
        messages.error(request, cm.RESTRICTED_PAGE)
        return redirect('personnel:permissions')

    if request.method == 'POST':
        form = GrantMultiplePermissionsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            permissions = data['permissions']
            personnels = data['personnels']

            for permission in permissions:
                for personnel in personnels:
                    permission.personnel.add(personnel)

            msg = "Permissions successfully granted"
            messages.success(request, msg)
            return redirect('personnel:permissions')
        else:
            return render(request, template, {'form' : form})

    return render(request, template, {'form' : GrantMultiplePermissionsForm()})

def report(request, out_format):
    """Return pdf or html output depending on the format specified in the url"""
    queryset = Personnel.objects.all()
    filename = 'Personnel report'

    if out_format == 'html':
        template = 'personnel/report_html.html'
        return report_view(
            request, queryset, filename, template, view=out_format)
    template = 'personnel/report_pdf.html'
    return report_view(request, queryset, filename, template, view=out_format)

class PersonnelDetail(generic.DetailView):
    model = Personnel
    context_object_name = 'personnel'
    template_name = 'personnel/detail.html'

class PersonnelPublicIndex(PaginationMixin, LoginRequiredMixin, generic.ListView):
    model = Personnel
    context_object_name = 'personnels'
    template_name = "personnel/staffers.html"
    paginate_by = 25

@login_required
def dashboard(request):
    context = {}
    context['personnel'] = request.user.personnel
    template = 'personnel/dashboard.html'
    return render(request, template, context)

@personnel_is_ceo_or_manager
def dashboard_manager(request):
    context = {}
    template = 'personnel/dashboard_manager.html'
    # user = request.user
    return render(request, template, context)

@personnel_is_ceo
def dashboard_ceo(request):
    context = {}
    template = 'personnel/dashboard_ceo.html'
    # user = request.user
    return render(request, template, context)

class BranchPersonnel(LoginRequiredMixin, PaginationMixin, generic.ListView):
    model = Personnel
    context_object_name = 'branch_staff'
    template_name = "personnel/branch_personnel.html"
    paginate_by = 25

    def get_queryset(self):
        return [each.personnel for each in BranchAccessCode.objects.filter(branch=get_branch(self.request))]

class GroupIndex(LoginRequiredMixin, PaginationMixin, generic.ListView):
    model = Group
    context_object_name = "groups"
    template_name = "personnel/groups.html"
    paginate_by = 10

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if rules.test_rule('view_group_index', user):
            return super().dispatch(*args, **kwargs)
        messages.error(self.request, cm.RESTRICTED_PAGE)
        return redirect('/')

@personnel_belongs_to_it
def new_group(request):
    template = "personnel/group_new.html"
    if request.method == "POST":
        form = NewGroupForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            name = form["name"]
            try:
                Group.objects.create(name=name)
            except IntegrityError:
                messages.error(request, 'Group already exists.')
                return redirect("/")
            return redirect("personnel:groups")
    else:
        form = NewGroupForm()
        return render(request, template, {"form" : form})

def personnel_remunerations(request, pk, slug):
    template = "bet9ja/remunerations.html"
    context = {}
    context["date_range_form"] = SelectDateRangeForm()
    context["remunerations"] = Remuneration.objects.filter(personnel__pk=pk, personnel__slug=slug)
    return render(request, template, context)

def personnel_remits(request, pk, slug):
    template = "bet9ja/remits.html"
    context = {}
    context["date_range_form"] = SelectDateRangeForm()
    context["remits"] = Remit.objects.filter(personnel__pk=pk, personnel__slug=slug)
    return render(request, template, context)

def personnel_gameremits(request, pk, slug):
    template = "game/gameremits.html"
    context = {}
    context["date_range_form"] = SelectDateRangeForm()
    context["gameremits"] = GameRemit.objects.filter(personnel__pk=pk, personnel__slug=slug)
    return render(request, template, context)

def personnel_viewcenterremits(request, pk, slug):
    template = "viewcenter/viewcenterremits.html"
    context = {}
    context["date_range_form"] = SelectDateRangeForm()
    context["viewcenterremits"] = ViewCenterRemit.objects.filter(personnel__pk=pk, personnel__slug=slug)
    return render(request, template, context)

def personnel_sales(request, pk, slug):
    template = "personnel/personnel_sales.html"
    context = {}
    context["sale_filter_form"] = PersonnelSaleFilterForm()
    context['manager_view'] = False
    context["sales"] = Sale.objects.filter(personnel__pk=pk, personnel__slug=slug)
    return render(request, template, context)

class PersonnelSaleFilterView(LoginRequiredMixin, PaginationMixin, generic.ListView):
    model = Sale
    template_name = "personnel/personnel_sales.html"
    context_object_name = "sales"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(PersonnelSaleFilterView, self).get_context_data(**kwargs)
        context['sale_filter_form'] = PersonnelSaleFilterForm()
        context['manager_view'] = True
        return context

    def get_queryset(self):
        if self.request.method == 'GET':
            form = PersonnelSaleFilterForm(self.request.GET)

            if form.is_valid():
                form = form.cleaned_data
                product = form['product']
                from_date = form['from_date']
                to_date = form['to_date']

                # build queries
                queries = []
                msg = []
                if product:
                    queries.append(Q(product=product))
                    msg.append('{}'.format(product))
                if from_date:
                    if not to_date:
                        to_date = from_date + timedelta(days=7)
                    queries.append(Q(created__range=[from_date, to_date]))
                    msg.append('Date {} to {}'.format(from_date, to_date))

                # combine queries
                try:
                    query = reduce(operator.and_, queries)
                    query_str = " AND ".join(msg)
                except TypeError:
                    query = []
                    query_str = ""

                # execute query
                messages.success(self.request, "Search results for {}".format(query_str))
                return Sale.objects.filter(query)

def personnel_expenditures(request, pk, slug):
    template = "bet9ja/expenditures.html"
    context = {}
    context["date_range_form"] = SelectDateRangeForm()
    context["expenditures"] = Expenditure.objects.filter(personnel__pk=pk, personnel__slug=slug)
    return render(request, template, context)

def personnel_debts(request, pk, slug):
    template = "account/debts.html"
    context = {}
    context["debts"] = Debt.objects.filter(personnel__pk=pk, personnel__slug=slug)
    return render(request, template, context)

def send_new_user_email(request, new_personnel):
    subject = "Welcome to FunnShopp"
    email = new_personnel.user.email
    creator = "{} {}".format(request.user.personnel.first_name, request.user.personnel.last_name)
    profile_link = request.build_absolute_uri(new_personnel.get_edit_url())
    receivers = [email, 'damianorji@gmail.com', 'orjichidi95@gmail.com']

    context = {}
    context['password'] = 'change-this-password'
    context['creator'] = creator
    context['new_user_email'] = email
    context['profile_link'] = profile_link

    text_email = render_to_string("personnel/new_user.txt", context)
    html_email = render_to_string("personnel/new_user.html", context)
    from_email = settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives(subject, text_email, from_email, receivers)
    msg.attach_alternative(html_email, "text/html")
    msg.send()

@check_recaptcha
def new_personnel(request):
    if rules.test_rule('create_new_user', request.user) is False:
        messages.error(request, cm.OPERATION_FAILED)
        return redirect('/')
    template = "personnel/personnel_new.html"
    if request.method == 'POST':
        form = PersonnelRegistrationForm(request.POST)
        if form.is_valid():
            if request.recaptcha_is_valid:
                form = form.cleaned_data
                display_name = form["display_name"]
                email = form['email_address']
                first_name = form['first_name']
                last_name = form['last_name']

                user = Person(email=email)
                user.set_password('change-this-password')
                user.is_active = True
                user.save()
                new_personnel = Personnel(user=user, display_name=display_name, first_name=first_name, last_name=last_name)
                new_personnel.save()

                send_new_user_email(request, new_personnel)
                messages.success(request, "Personnel successfully created.")
                return redirect(reverse("personnel:edit_by_manager", kwargs={'pk' : new_personnel.pk,  'slug' : new_personnel.slug}))
            else:
                form.add_error(None, 'Error: Please complete the reCAPTCHA.')
                return render(request, template, {'form' : form})
    else:
        form = PersonnelRegistrationForm()
    return render(request, template, {'form' : form})

@login_required
def welcome_personnel(request, display_name):
    template = 'personnel/create_success.html'
    context = {'display_name' : display_name}
    return render(request, template, context)

@personnel_is_ceo_or_manager
def activate_personnel(request, display_name, pk):
    user = Person.objects.get(pk=pk)
    context = {}
    if user.is_active:
        personnel = Personnel.objects.get(user=user)
        context["active"] = "active"
        context["personnel"] = personnel
    else:
        user.is_active = True
        user.save()
        personnel = Personnel.objects.get(user=user)
        context["personnel"] = personnel
    context["display_name"] = display_name
    messages.success(request, "{} was successfully activated".format(personnel.display_name))
    return render(request, "personnel/create_activation.html", context)

@personnel_is_ceo
def activate_deactivate_personnel_account(request, pk, slug):
    if rules.test_rule('activate_deactivate_personnel_account', request.user) is False:
        messages.error(request, cm.OPERATION_FAILED)
        return redirect('personnel:index')

    personnel = Personnel.objects.get(pk=pk, slug=slug)
    person = personnel.user
    if person.is_active:
        person.is_active = False
        msg = "{} successfully deactivated".format(personnel.display_name)
    else:
        person.is_active = True
        msg = "{} successfully activated".format(personnel.display_name)
    person.save()
    messages.success(request, msg)
    return redirect(reverse("personnel:index"))

def add_personnels_to_group(request, pk):
    """Recursively add personnels to a group"""
    template = "personnel/group_add_personnel.html"
    group = Group.objects.get(pk=pk)

    if rules.test_rule('group_add_personnel', request.user) is False:
        messages.error(request, cm.RESTRICTED_PAGE)
        return redirect('/')

    if group.name == 'CEO' and (rules.test_rule('is_ceo', request.user) is False): # restrict addition to CEO group
        messages.error(request, cm.OPERATION_FAILED)
        return redirect("/")
    if group.name == 'IT' and not request.user.is_admin: # restrict addition to IT group
        messages.error(request, cm.OPERATION_FAILED)
        return redirect("/")
    if group.name == 'Manager' and (rules.test_rule('is_ceo', request.user) is False): # only CEO can add user to manager
        messages.error(request, cm.OPERATION_FAILED)
        return redirect("/")

    msg = []
    if request.method == "POST":
        form = AddPersonnelToGroupForm(request.POST, group_name=group.name)
        if form.is_valid():
            personnels = [Personnel.objects.get(pk=pk) for pk in request.POST.getlist("personnels", "")]

            for personnel in personnels:
                personnel.user.groups.add(group)
                msg.append(personnel.display_name)
            msg = "Added {} to {}".format(", ".join(msg), group.name)
            messages.success(request, msg)
            return redirect("personnel:groups")
    else:
        form = AddPersonnelToGroupForm(group_name=group.name)
        return render(request, template, {"form" : form, "group" : group})

def remove_personnel_from_group(request, pk):
    """Recursively remove personnels from a group"""
    template = "personnel/group_remove_personnel.html"
    group = Group.objects.get(pk=pk)

    if rules.test_rule('group_remove_personnel', request.user) is False:
        messages.error(request, cm.RESTRICTED_PAGE)
        return redirect('/')

    if group.name == 'CEO' and (rules.test_rule('is_ceo', request.user) is False): # restrict addition to CEO group
        messages.error(request, cm.RESTRICTED_PAGE)
        return redirect("/")
    if group.name == 'IT' and not request.user.is_admin: # restrict addition to IT group
        messages.error(request, cm.RESTRICTED_PAGE)
        return redirect("/")
    if group.name == 'Manager' and (rules.test_rule('is_ceo', request.user) is False): # only CEO can add user to manager
        return redirect("/")

    msg = []

    if request.method == "POST":
        form = RemovePersonnelFromGroupForm(request.POST, group_name=group.name)
        if form.is_valid():
            personnels = [Personnel.objects.get(pk=pk) for pk in request.POST.getlist("personnels", "")]

            for personnel in personnels:
                personnel.user.groups.remove(group)
                msg.append(personnel.display_name)
            msg = "{} removed from  {}".format(", ".join(msg), group.name)
            messages.success(request, msg)
            return redirect("personnel:groups")
    else:
        form = RemovePersonnelFromGroupForm(group_name=group.name)
        return render(request, template, {"form" : form, "group" : group})

# never to be used. Only site administrator should be a staff
@personnel_is_ceo_or_manager
def make_staff(request, pk):
    person = Person.objects.get(pk=pk)
    if person.is_admin:
        person.is_admin = False
    else:
        person.is_admin = True
    person.save()
    return redirect("personnel:index")

class PersonnelEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Personnel
    form_class = PersonnelEditForm
    template_name = 'personnel/edit.html'
    success_message = "Profile updated successfully."

    def get_success_url(self):
        return reverse("personnel:dashboard")

@method_decorator(personnel_is_ceo_or_manager, name='dispatch')
class PersonnelEditByManager(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Personnel
    form_class = PersonnelEditByManagerForm
    template_name = 'personnel/personnel_edit_by_manager.html'
    success_message = "You've successfully updated a personnel profile"

class PersonnelAvatarCreate(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Personnel
    form_class = PersonnelAvatarAddForm
    template_name = "personnel/new_avatar.html"
    success_message = "You've successfully added an avatar."

    def get_success_url(self):
        return reverse("personnel:dashboard")

class PersonnelAvatarEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Personnel
    form_class = PersonnelAvatarAddForm
    template_name = "personnel/edit_avatar.html"
    success_message = "Avatar successfully updated."

    def get_success_url(self):
        return reverse("personnel:dashboard")

class PersonnelAddSuccess(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Personnel
    form_class = PersonnelEditForm
    template_name = 'personnel/create_success.html'
    success_message = "New personnel successfully created."
