from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexView, name='index'),
    path('doctors/', views.doctorListView, name='doctor-list'),
    path('doctor/<int:id>', views.doctorDetailView, name='doctor-detail'),
    path('doctor/create', views.createDoctorView, name='create-doctor'),
    path('doctor/edit/<int:id>', views.editDoctorView, name='edit-doctor'),
    path('doctor/delete/<int:id>', views.deleteDoctorView, name='delete-doctor'),

    path('patients/', views.patientListView, name='patient-list'),
    path('patient/<int:id>', views.patientDetailView, name='patient-detail'),
    path('patient/create', views.createPatientView, name='create-patient'),
    path('patient/edit/<int:id>', views.editPatientView, name='edit-patient'),
    path('patient/delete/<int:id>', views.deletePatientView, name='delete-patient'),

    path('appointments/', views.appointmentListView, name='appointment-list'),
    path('appointment/<int:id>', views.appointmentDetailView, name='appointment-detail'),
    path('appointment/create', views.createAppointmentView, name='create-appointment'),
    path('appointment/edit/<int:id>', views.editAppointmentView, name='edit-appointment'),
    path('appointment/delete/<int:id>', views.deleteAppointmentView, name='delete-appointment'),

    path('registration-doctor/', views.doctorRegistration, name='doctor-registration'),
    
]