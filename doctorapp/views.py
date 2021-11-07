from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from adminapp.views import patientDetailView
from hospital.models import *
from django.contrib.auth import authenticate,logout,login
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect

from .forms import ManageAppointmentForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def doctorRegistration(request):
    error = ""
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        birthdate = request.POST['dateofbirth']
        department = request.POST['department']
        phonenumber = request.POST['phonenumber']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        address = request.POST['address']

        if password == repeatpassword:
            user = User.objects.create_user(username=email, first_name=first_name, last_name=last_name, email=email, password = password)

            doc_grp = Group.objects.get_or_create(name = 'Doctors')[0]
            doc_grp.user_set.add(user)
            user.save()

            doctor = Doctor.objects.create(user=user, first_name=first_name, last_name=last_name, gender=gender, dob=birthdate, department=department, phone=phonenumber, address=address, email=email)
            messages.success(request, "Doctor account created.")
            return redirect('index')

        else:
            messages.error(request, "Passwords do not match")

    context = {'error' : error}
    return render(request, 'doctorapp/doctor_registration.html', context)

def dashboardView(request):
    return render(request, 'doctorapp/dashboard.html')

def loginView(request):
    error = ""
    page = ""

    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(request,username=u,password=p)

        if user is not None:
            if not user.groups.filter(name = 'Doctors').exists():
                messages.error(request, "You are not a Doctor")
                return redirect('index')
            login(request,user)
            error = "no"
            return redirect('doctor-dashboard')

        else:
            error = "yes"
            messages.error(request, 'Invalid Credentials')
        
    context = {'error': error}
    print(error)
    return render(request,'doctorapp/login.html',context)

def logoutView(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect('index')

def myAppointmentsView(request):
    doctor = request.user.doctor
    upcoming_appointments = doctor.appointment_set.filter(confirmed=True).filter(completed=False)
    completed_appointments = doctor.appointment_set.filter(completed=True)

    context = {
        'doctor': doctor,
        'upcoming_appointments': upcoming_appointments,
        'completed_appointments': completed_appointments,
    }
    return render(request, 'doctorapp/my_appointments.html', context)

def manageAppointmentView(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    form = ManageAppointmentForm(instance=appointment)

    if(request.method == 'POST'):
        form = ManageAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('doctor-appointments')

    context = {
        'appointment': appointment,
        'form': form
    }
    return render(request, 'doctorapp/manage_appointment.html', context)
