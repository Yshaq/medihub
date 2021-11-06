from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboardView, name='patient-dashboard'),
    path('login/', views.loginView, name='patient-login'),
    path('logout/', views.logoutView, name='patient-logout'),
    path('register/', views.patientRegistration, name='patient-register'),
]