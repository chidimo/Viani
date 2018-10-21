from django.contrib import admin

from .models import Job, JobExpense, JobPayment

admin.site.register(Job)
admin.site.register(JobExpense)
admin.site.register(JobPayment)
