from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

import rules
from .utils import context_messages as cm

from .models import Job
from .forms import NewJobForm

def gallery(request):
    template = 'shop/gallery.html'
    context = {}
    return render(request, template, context)

class NewJob(LoginRequiredMixin, generic.CreateView):
    model = Job
    form_class = NewJobForm
    template_name = 'shop/job_new.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if rules.test_rule('create_new_job', user):
            return super().dispatch(request, *args, **kwargs)
        messages.error(self.request, cm.OPERATION_FAILED)
        return redirect('/')
