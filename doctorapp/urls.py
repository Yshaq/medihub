from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboardView, name='doctor-dashboard'),
    path('login/', views.loginView, name='doctor-login'),
    path('logout/', views.logoutView, name='doctor-logout'),
    path('register/', views.doctorRegistration, name='doctor-register'),
]