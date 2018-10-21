from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('gallery/', views.gallery, name='gallery')
]
