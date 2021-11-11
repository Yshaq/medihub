from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboardView, name='doctor-dashboard'),
    path('login/', views.loginView, name='doctor-login'),
    path('logout/', views.logoutView, name='doctor-logout'),
    path('register/', views.doctorRegistration, name='doctor-register'),

    path('appointments/', views.myAppointmentsView, name='doctor-appointments'),
    path('appointments/<int:id>', views.appointmentDetailView, name='doctor-appointment-detail'),
    path('appointments/<int:id>/manage', views.manageAppointmentView, name='doctor-manage-appointment'),

    path('patients/', views.patientListView, name='doctor-patient-list'),
    path('patients/<int:id>', views.patientDetailView, name='doctor-patient-detail'),
]