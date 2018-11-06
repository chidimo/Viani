from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = []

urlpatterns += [
    path('gallery/', views.gallery, name='gallery'),
]

urlpatterns += [
    path('customer-index/', views.CustomerIndex.as_view(), name='customer_index'),
    path('new-customer', views.NewCustomer.as_view(), name='customer_new'),
    path('customer/<int:pk>/', views.customer_details, name='customer_details'),
    path('edit-customer/<int:pk>/', views.EditCustomer.as_view(), name='edit_customer'),
]

urlpatterns += [
    path('job-index/', views.JobIndex.as_view(), name='job_index'),
    path('job-new/', views.NewJob.as_view(), name='job_new'),
    path('job-edit/<int:pk>/', views.EditJob.as_view(), name='job_edit'),
    path('job/<int:pk>/', views.JobDetail.as_view(), name='job_detail'),
    path('add-cashflow/<int:pk>/', views.job_add_cashflow, name='job_add_cashflow'),
    path('update-status/<int:pk>/', views.UpdateJobStatus.as_view(), name='job_update_status'),
]

urlpatterns += [
    path('new-cashflowtype/', views.NewCashFlowType.as_view(), name='cashflowtype_new'),
    path('cashflowtype-index/', views.CashFlowTypeIndex.as_view(), name='cashflowtype_index'),
    path('new-cashflow/', views.NewCashFlow.as_view(), name='cashflow_new'),
    path('cashflow-index/', views.CashFlowIndex.as_view(), name='cashflow_index'),
    path('bank-cashflow/<int:pk>/', views.bank_cashflow, name='bank_cashflow'),
]
