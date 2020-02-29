from django.urls import path
from . import views

app_name = 'account'

urlpatterns = []

urlpatterns += [
    path('revenues/', views.RevenueIndex.as_view(), name='revenues'),
    path('revenue/payment/<int:pk>/', views.add_revenue_to_job, name='add_revenue_to_job'),

]

urlpatterns += [
    # path('expendituretypes/', views.ExpenditureIndex.as_view(), name='expenditure_types'),
    path('expendituretype/new/', views.NewExpenditureType.as_view(), name='new_expenditure_type'),
]

urlpatterns += [
    path('expenditures/', views.ExpenditureIndex.as_view(), name='expenditures'),
    path('expenditures/new', views.NewExpenditure.as_view(), name='new_expenditure'),
    path('expenditures/expense/<int:pk>/', views.add_expenditure_to_job, name='add_expenditure_to_job'),
]

urlpatterns += [
    path('accounting/', views.accounting, name='accounting')
]
