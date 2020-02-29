from django.urls import path
from . import views

app_name = 'account'

urlpatterns = []

urlpatterns += [
    path('revenues/index/', views.RevenueIndex.as_view(), name='revenues'),
    path('expenditures/index/', views.ExpenditureIndex.as_view(), name='expenditures'),
]

