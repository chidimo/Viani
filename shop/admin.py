from django.contrib import admin

from .models import Customer, Job

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'address', 'sex')

class JobAdmin(admin.ModelAdmin):
    list_display = ('description', 'status', 'customer', 'value', 'discount', 'total_payment', 'total_expenditure', 'net_profit', 'start_date', 'completed', 'notes')
    list_editable = ('customer', 'value', 'discount', 'status', 'start_date', 'completed', 'notes' )

admin.site.register(Job, JobAdmin)
admin.site.register(Customer, CustomerAdmin)
