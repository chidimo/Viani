from django.contrib import admin

from .models import ExpenditureType, Expenditure, MonthCheck


class ExpenditureTypeAdmin(admin.ModelAdmin):
    list_display = ('created', 'name', 'description')


class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ('created', 'date', 'personnel',
                    'amount', 'category', 'notes')


class MonthCheckAdmin(admin.ModelAdmin):
    list_display = ('created', 'month', 'year', 'value', 'personnel')


admin.site.register(MonthCheck, MonthCheckAdmin)
admin.site.register(Expenditure, ExpenditureAdmin)
admin.site.register(ExpenditureType, ExpenditureTypeAdmin)
