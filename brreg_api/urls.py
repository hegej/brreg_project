from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bankrupt-companies/', views.bankrupt_companies, name='bankrupt_companies'),
    path('as-companies/', views.as_companies, name='as_companies'),
    path('get-as-count/', views.get_as_count, name='get_as_count'), 
]