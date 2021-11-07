from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboardView, name='doctor-dashboard'),
    path('login/', views.loginView, name='doctor-login'),
    path('logout/', views.logoutView, name='doctor-logout'),
    path('register/', views.doctorRegistration, name='doctor-register'),

    path('appointments/', views.myAppointmentsView, name='doctor-appointments'),
    path('appointments/<int:id>', views.manageAppointmentView, name='doctor-manage-appointment'),
]