"""Utility functions"""
from itertools import filterfalse

from django.apps import apps
from django.shortcuts import redirect
from django.contrib import messages

from personnel.models import Personnel

MY_APPS = ("asset", "bet9ja", "establishment", "personnel", "service")

def get_model_list():
    "Get models defined in project as a list of tuples"
    app_labels = []
    all_apps = apps.all_models
    for app, models in all_apps.items():
        for model_name, model_class in models.items():
            if app in MY_APPS:
                display = "{}-{}".format(app, model_name)
                app_model = (app, model_name)
                app_labels.append((app_model, display))
                # print("{}, {}".format(app_model, display))
    return app_labels

def user_is_self():
    pass

def personnel_is_self_or_ceo(func):
    def check_and_call(request, *args, **kwargs):
        user = request.user
        pk = kwargs.get('pk', None)
        slug = kwargs.get('slug', None)

        personnel = Personnel.objects.get(pk=pk, slug=slug)

        if any(
            [
                personnel.user==user,
                user.groups.filter(name__in=['CEO']).exists()
             ]):
            return func(request, *args, **kwargs)
            messages.error(request, 'Access denied')
        return redirect('/')
    return check_and_call

# personnel_is_self_or_user_supervisor
def personnel_is_self_or_manager(func):
    def check_and_call(request, *args, **kwargs):
        user = request.user
        pk = kwargs.get('pk', None)
        slug = kwargs.get('slug', None)

        personnel = Personnel.objects.get(pk=pk, slug=slug)

        if any(
            [
                user.groups.filter(name__in=['Manager']).exists(),
                # personnel.supervisor.user==user
            ]):
            return func(request, *args, **kwargs)
        messages.error(request, 'Access denied')
        return redirect('/')
    return check_and_call

# def personnel_is_self_user_supervisor_or_ceo
def personnel_is_self_ceo_or_manager(func):
    def check_and_call(request, *args, **kwargs):
        user = request.user
        pk = kwargs.get('pk', None)
        slug = kwargs.get('slug', None)

        accessor = Personnel.objects.get(user=user)
        personnel = Personnel.objects.get(pk=pk, slug=slug)

        if any(
            [
                personnel.user==user,
                # personnel.supervisor==accessor,
                user.groups.filter(name__in=['CEO']).exists()
            ]):
            return func(request, *args, **kwargs)
        messages.error(request, 'Access denied')
        return redirect('/')
    return check_and_call

# personnel_belongs_to_ceo_or_manager
def personnel_is_ceo_or_manager(func):
    def check_and_call(request, *args, **kwargs):
        user = request.user

        if user.groups.filter(name__in=['CEO', 'Manager']).exists():
            return func(request, *args, **kwargs)
        messages.error(request, 'Access denied')
        return redirect('/')
    return check_and_call

# personnel_belongs_to_ceo
def personnel_is_ceo(func):
    def check_and_call(request, *args, **kwargs):
        user = request.user

        if user.groups.filter(name__in=['CEO']).exists():
            return func(request, *args, **kwargs)
        messages.error(request, 'Access denied')
        return redirect('/')
    return check_and_call

def personnel_belongs_to_it(func):
    def check_and_call(request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name__in=['it']).exists():
            return func(request, *args, **kwargs)
        messages.error(request, "You're not authorized to perform this operation.")
        return redirect('/')
    return check_and_call

# personnel_belongs_to_manager
def personnel_is_manager(func):
    def check_and_call(request, *args, **kwargs):
        user = request.user

        if user.groups.filter(name__in=['Manager']).exists():
            return func(request, *args, **kwargs)
        messages.error(request, 'Access denied')
        return redirect('/')
    return check_and_call

def unique_everseen(iterable, key=None):
    """List unique elements, preserving order. Remember all elements ever seen.
    source: https://docs.python.org/3/library/itertools.html#itertools-recipes"""
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

if __name__ == "__main__":
    get_model_list()
