from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboardView, name='admin-dashboard'),

    path('login/', views.loginView, name='admin-login'),
    path('logout/', views.logoutView, name='admin-logout'),

    path('manage-appointments', views.manageAppointmentsList, name='manage-appointments-list'),
    path('manage-appointments/<int:id>', views.manageAppointment, name='manage-appointment'),

    path('bills/', views.billListView, name='admin-bills'),
    path('bills/generate', views.generateBillView, name='generate-bill'),
    path('bills/<int:id>', views.billPdfView, name='admin-bill'),
    path('bills/<int:id>/setpay', views.billSetPaid, name='bill-set-paid'),

    path('crud/', views.crudIndex, name='crud-index'),

    path('crud/doctors/', views.doctorListView, name='doctor-list'),
    path('crud/doctor/<int:id>', views.doctorDetailView, name='doctor-detail'),
    path('crud/doctor/create', views.createDoctorView, name='create-doctor'),
    path('crud/doctor/edit/<int:id>', views.editDoctorView, name='edit-doctor'),
    path('crud/doctor/delete/<int:id>', views.deleteDoctorView, name='delete-doctor'),

    path('crud/patients/', views.patientListView, name='patient-list'),
    path('crud/patient/<int:id>', views.patientDetailView, name='patient-detail'),
    path('crud/patient/create', views.createPatientView, name='create-patient'),
    path('crud/patient/edit/<int:id>', views.editPatientView, name='edit-patient'),
    path('crud/patient/delete/<int:id>', views.deletePatientView, name='delete-patient'),

    path('crud/appointments/', views.appointmentListView, name='appointment-list'),
    path('crud/appointment/<int:id>', views.appointmentDetailView, name='appointment-detail'),
    path('crud/appointment/create', views.createAppointmentView, name='create-appointment'),
    path('crud/appointment/edit/<int:id>', views.editAppointmentView, name='edit-appointment'),
    path('crud/appointment/delete/<int:id>', views.deleteAppointmentView, name='delete-appointment'),


]