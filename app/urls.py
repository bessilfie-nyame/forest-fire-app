from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("account/", include("django.contrib.auth.urls"),
    name='login'),
    path("logout", views.logout_request, name="logout"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('dashboard/', views.DashboardView.as_view(), 
    name='dashboard'),
    path('result/<prediction>', views.result, name='result')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)