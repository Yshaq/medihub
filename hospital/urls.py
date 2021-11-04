from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexView, name='index'),
    path('doctors/', views.doctorListView, name='doctor-list'),
    path('doctor/<int:id>', views.doctorDetailView, name='doctor-detail'),
    path('doctor/create', views.createDoctorView, name='create-doctor'),
    path('doctor/edit/<int:id>', views.editDoctorView, name='edit-doctor'),
    path('doctor/delete/<int:id>', views.deleteDoctorView, name='delete-doctor'),
    path('login/', views.loginpage, name='Login-page'),
    path('create_account/', views.createaccountpage, name='create_account-page'),
]