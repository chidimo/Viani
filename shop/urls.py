from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('gallery/', views.gallery, name='gallery')
]

urlpatterns += [
    path('new-job/', views.NewJob.as_view(), name='job_new')
]
