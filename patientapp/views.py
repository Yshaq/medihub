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
from django.contrib.auth.decorators import login_required

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

def profile(request):
    if not request.user.is_active:
        return redirect('login_page')
    patient = get_object_or_404(Patient, email=request.user)
    context = {
        'patient': patient,
    }
    return render(request, 'patientapp/profile.html', context)

@login_required(login_url='patient-login')
def doctorListView(request):
    doctorList = Doctor.objects.all()
    context = {
        'list_of_doctors': doctorList,
    }
    return render(request, 'patientapp/doctor_list.html', context)

def bookappointment(request,id):
    patient = get_object_or_404(Patient, email=request.user)
    doctor=get_object_or_404(Doctor,pk=id)
    error=""
    if request.method == 'POST':
        # try:
            date=request.POST["date"]
            appointment = Appointment.objects.create( doctor=doctor,patient=patient,date=date)
            messages.success(request,"Appointment requested")
            return redirect('patient_views_doctor_list')
        # except:
        #     error="yes"
            
    context = {
        
        'doctor':doctor,
        'patient':patient,
        
    }
    return render(request, 'patientapp/appointments.html', context)
def myappointments(request):
    patient = get_object_or_404(Patient, email=request.user)
    appointments=Appointment.objects.all().filter(patient=patient)
    context={
        'appointments':appointments
    }
    return render(request,'patientapp/myappointments.html',context)
def myappointmentdetails(request,id):
    appointment =get_object_or_404(Appointment, pk=id)
    context={
        'appointment':appointment
    }
    return render(request,'patientapp/myappointmentdetails.html',context)

def billPdfView(request, id):
    bill = Bill.objects.get(pk=id)
    itemmap = bill.billitemmap_set.all()
    context = {
        'bill': bill,
        'itemmap': itemmap,
    }
    return render(request, 'patientapp/billpdf.html', context)

def billListView(request):
    patient = get_object_or_404(Patient, user=request.user)
    my_bills = patient.bill_set.all()
    unpaid_bills = my_bills.filter(paid=False)
    paid_bills = my_bills.filter(paid=True)
    context = {
        'unpaid_bills': unpaid_bills,
        'paid_bills': paid_bills,
    }
    return render(request, 'patientapp/bill_list.html', context)
