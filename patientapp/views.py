from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from hospital.models import *
from django.contrib.auth import authenticate,logout,login
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect

from hospital.forms import DoctorForm, PatientForm, AppointmentForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def loginView(request):
    error = ""
    page = ""

    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(request,username=u,password=p)

        if user is not None:
            if not user.groups.filter(name = 'Patients').exists():
                messages.error(request, "You are not a Patient")
                return redirect('index')
            login(request,user)
            error = "no"
            return redirect('patient-dashboard')

        else:
            error = "yes"
            messages.error(request, 'Invalid Credentials')
        
    context = {'error': error}
    print(error)
    return render(request,'patientapp/login.html',context)

def logoutView(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect('index')

def dashboardView(request):
    return render(request, 'patientapp/dashboard.html')

def patientRegistration(request):
    error = ""
    user="none"
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']

        if password == repeatpassword:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,username=email, password=password)

            patient = Patient.objects.create(user=user, first_name=first_name,last_name=last_name,email=email, gender=gender,phone=phonenumber,address=address,dob=birthdate)

            pat_group = Group.objects.get_or_create(name='Patients')[0]
            pat_group.user_set.add(user)
            #print(pat_group)
            user.save()
            messages.success(request, "Patient created successfully!")
            #print(user)
            error = "no"
            return redirect('index')
        else:
            messages.error(request, "Passwords do not match")
            error = "yes"
                    
    context = {'error' : error}
    #print(error)
    return render(request,'patientapp/patientregistration.html',context)