from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboardView, name='patient-dashboard'),
    path('login/', views.loginView, name='patient-login'),
    path('logout/', views.logoutView, name='patient-logout'),
    path('register/', views.patientRegistration, name='patient-register'),
    path('profile/',views.profile,name='profile'),
    path('doctor_list/',views.doctorListView,name='patient_views_doctor_list'),
    path('book_appointment/<int:id>',views.bookappointment,name='book-appointment'),
    path('myappointments/',views.myappointments,name='my_appointments'),
    path('myappointmentdetail/<int:id>',views.myappointmentdetails,name='my_appointment_detail'),

    path('bills/', views.billListView, name='patient-bill-list'),
    path('bills/<int:id>', views.billPdfView, name='patient-bill'),
]