from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = []

urlpatterns += [
    path('customers/index/', views.CustomerIndex.as_view(), name='customer_index'),
    path('customers/new/', views.NewCustomer.as_view(), name='customer_new'),
    path('customers/<int:pk>/', views.customer_details, name='customer_details'),
    path('customers/edit/<int:pk>/', views.EditCustomer.as_view(), name='edit_customer'),
]

urlpatterns += [
    path('jobs/index/', views.JobIndex.as_view(), name='job_index'),
    path('jobs/new/', views.NewJob.as_view(), name='job_new'),
    path('jobs/edit/<int:pk>/', views.EditJob.as_view(), name='job_edit'),
    path('jobs/<int:pk>/', views.JobDetail.as_view(), name='job_detail'),
    path('jobs/add-cashflow/<int:pk>/', views.job_add_cashflow, name='job_add_cashflow'),
    path('jobs/update-status/<int:pk>/', views.UpdateJobStatus.as_view(), name='job_update_status'),
    path('jobs/mark-accepted/<int:pk>', views.mark_accepted, name='job_mark_accepted'),
    path('jobs-filter', views.JobFilterView.as_view(), name='job_filter'),
]

urlpatterns += [
    path('cashflowtype/new/', views.NewCashFlowType.as_view(), name='cashflowtype_new'),
    path('cashflowtype/index/', views.CashFlowTypeIndex.as_view(), name='cashflowtype_index'),
    path('cashflow/new/', views.NewCashFlow.as_view(), name='cashflow_new'),
    path('cashflow/index/', views.CashFlowIndex.as_view(), name='cashflow_index'),
    path('cashflow/bank/<int:pk>/', views.bank_cashflow, name='bank_cashflow'),
    path('cashflow-filter', views.CashFlowFilterView.as_view(), name='cashflow_filter'),
]

urlpatterns += [
    path('accounting/', views.accounting, name='accounting')
]
