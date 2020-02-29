from django.urls import path
from . import views

app_name = 'account'

urlpatterns = []

urlpatterns += [
    path('revenues/', views.RevenueIndex.as_view(), name='revenues'),
    path('expenditures/', views.ExpenditureIndex.as_view(), name='expenditures'),
]

