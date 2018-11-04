from django.contrib import admin

from .models import Customer, Job, CashFlowType, CashFlow

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'address', 'sex')

class JobAdmin(admin.ModelAdmin):
    list_display = ('customer', 'value', 'discount', 'total_expense', 'total_payment', 'start', 'completion', 'status', 'feedback')

class CashFlowTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class CashFlowAdmin(admin.ModelAdmin):
    list_display = ('job', 'name', 'category', 'amount', 'banked', 'notes')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(CashFlowType, CashFlowTypeAdmin)
admin.site.register(CashFlow, CashFlowAdmin)

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver

