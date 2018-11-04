from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = []

urlpatterns += [
    path('gallery/', views.gallery, name='gallery'),
]

urlpatterns += [
    path('customer-index', views.CustomerIndex.as_view(), name='customer_index'),
    path('new-customer', views.NewCustomer.as_view(), name='customer_new')
]

urlpatterns += [
    path('job-index/', views.JobIndex.as_view(), name='job_index'),
    path('new-job/', views.NewJob.as_view(), name='job_new'),
]

urlpatterns += [
    path('new-cashflowtype/', views.NewCashFlowType.as_view(), name='cashflowtype_new'),
    path('cashflowtype-index/', views.CashFlowTypeIndex.as_view(), name='cashflowtype_index'),
    path('new-cashflow/', views.NewCashFlow.as_view(), name='cashflow_new'),
    path('cashflow-index/', views.CashFlowIndex.as_view(), name='cashflow_index'),
    path('bank-cashflow/<int:pk>/', views.bank_cashflow, name='bank_cashflow'),
]
