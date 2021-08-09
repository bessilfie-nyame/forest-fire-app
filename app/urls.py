from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.DashboardView.as_view(), 
    name='dashboard'),
    path('result/<prediction>', views.result, name='result')
]