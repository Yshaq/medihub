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
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import ManageAppointmentForm

# Create your views here.
#===============UTILITY==================
def check_admin(user):
    if not user.groups.filter(name = 'Administrator').exists():
        return redirect('index')

#=========================================

@login_required(login_url='admin-login')
def dashboardView(request):
	return render(request,'adminapp/dashboard.html')

def loginView(request):
    error = ""
    page = ""

    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(request,username=u,password=p)

        if user is not None:
            if not user.groups.filter(name = 'Administrators').exists():
                messages.error(request, "You are not an Admin")
                return redirect('index')
            login(request,user)
            error = "no"
            return redirect('admin-dashboard')

        else:
            error = "yes"
            messages.error(request, 'Invalid Credentials')
        
    context = {'error': error}
    print(error)
    return render(request,'adminapp/login.html',context)

def logoutView(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect('index')

def manageAppointmentsList(request):
    requested_appointments = Appointment.objects.filter(completed=False).filter(confirmed=False)
    confirmed_appointments = Appointment.objects.filter(completed=False).filter(confirmed=True)
    context = {
        'requested_appointments': requested_appointments,
        'confirmed_appointments': confirmed_appointments,
    }
    return render(request, 'adminapp/manage_appointments_list.html', context)

def manageAppointment(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    form = ManageAppointmentForm(instance=appointment)

    if(request.method == 'POST'):
        form = ManageAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('manage-appointments-list')

    context = {
        'appointment': appointment,
        'form': form
    }
    return render(request, 'adminapp/manage_appointment.html', context)

def crudIndex(request):
    return render(request, 'adminapp/crud_index.html')

def billListView(request):
    unpaid_bills = Bill.objects.filter(paid=False)
    paid_bills = Bill.objects.filter(paid=True)
    context = {
        'unpaid_bills': unpaid_bills,
        'paid_bills': paid_bills,
    }
    return render(request, 'adminapp/bill_list.html', context)

def generateBillView(request):
    bill_items = Item.objects.all()

    if request.method == 'POST':
        patient_number = request.POST['patno']
        patient = get_object_or_404(Patient, pk=patient_number)
        bill = Bill.objects.create(patient=patient)

        total = 0
        fieldno = 1
        while(f'item{fieldno}' in request.POST):
            item_no = request.POST[f'item{fieldno}']
            qty = int(request.POST[f'qty{fieldno}'])
            item = get_object_or_404(Item, pk=item_no)
            BillItemMap.objects.create(bill=bill, item=item, qty=qty)
            total = total + item.price * qty
            fieldno = fieldno + 1

        bill.total = total
        bill.save()
        return redirect('admin-bills')

    context = {
        'bill_items': bill_items,
    }
    return render(request, 'adminapp/generate_bill.html', context)

def billPdfView(request, id):
    bill = Bill.objects.get(pk=id)
    itemmap = bill.billitemmap_set.all()
    context = {
        'bill': bill,
        'itemmap': itemmap,
    }
    return render(request, 'adminapp/billpdf.html', context)


def billSetPaid(request, id):
    bill = get_object_or_404(Bill, pk = id)
    bill.paid = True
    bill.save()
    return redirect('admin-bills')

#=================================================
#           DOCTOR MODEL CRUD
#=================================================
@login_required(login_url='admin-login')
def doctorListView(request):
    doctorList = Doctor.objects.all()
    context = {
        'list_of_doctors': doctorList,
    }
    return render(request, 'adminapp/doctor_list.html', context)

@login_required(login_url='admin-login')
def doctorDetailView(request, id):
    doctor = get_object_or_404(Doctor, pk=id)
    context = {
        'doctor': doctor,
    }
    return render(request, 'adminapp/doctor_detail.html', context)

@login_required(login_url='admin-login')
def createDoctorView(request):
    form = DoctorForm()
    if (request.method == 'POST'):
        form = DoctorForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('doctor-list')
        else:
            messages.error(request, 'invalid form')

    context = {
        'form': form,
    }
    return render(request, 'adminapp/model_form.html', context)

@login_required(login_url='admin-login')
def editDoctorView(request, id):
    doctor = get_object_or_404(Doctor, pk=id)
    form = DoctorForm(instance=doctor)

    if (request.method == 'POST'):
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor-list')

    context = {
        'form': form,
    }

    return render(request, 'adminapp/model_form.html', context)

@login_required(login_url='admin-login')
def deleteDoctorView(request, id):
    doctor = get_object_or_404(Doctor, pk=id)
    if(request.method == 'POST'):
        doctor.delete()
        return redirect('doctor-list')

    context = {
        'doctor': doctor,
    }
    return render(request, 'adminapp/delete_doctor.html', context)

#=================================================
#           PATIENT MODEL CRUD
#=================================================

@login_required(login_url='admin-login')
def patientListView(request):
    patientList = Patient.objects.all()
    context = {
        'list_of_patients': patientList,
    }
    return render(request, 'adminapp/patient_list.html', context)

@login_required(login_url='admin-login')
def patientDetailView(request, id):
    patient = get_object_or_404(Patient, pk=id)
    context = {
        'patient': patient,
    }
    return render(request, 'adminapp/patient_detail.html', context)

@login_required(login_url='admin-login')
def createPatientView(request):
    form = PatientForm()
    if (request.method == 'POST'):
        form = PatientForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('patient-list')
        else:
            messages.error(request, 'invalid form')

    context = {
        'form': form,
    }
    return render(request, 'adminapp/model_form.html', context)

@login_required(login_url='admin-login')
def editPatientView(request, id):
    patient = get_object_or_404(Patient, pk=id)
    form = PatientForm(instance=patient)

    if (request.method == 'POST'):
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient-list')

    context = {
        'form': form,
    }

    return render(request, 'adminapp/model_form.html', context)

@login_required(login_url='admin-login')
def deletePatientView(request, id):
    patient = get_object_or_404(Patient, pk=id)
    if(request.method == 'POST'):
        patient.delete()
        return redirect('patient-list')

    context = {
        'patient': patient,
    }
    return render(request, 'adminapp/delete_patient.html', context)

#=================================================
#           APPOINTMENT MODEL CRUD
#=================================================

@login_required(login_url='admin-login')
def appointmentListView(request):
    appointmentList = Appointment.objects.all()
    context = {
        'list_of_appointments': appointmentList,
    }
    return render(request, 'adminapp/appointment_list.html', context)

@login_required(login_url='admin-login')
def appointmentDetailView(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    context = {
        'appointment': appointment,
    }
    return render(request, 'adminapp/appointment_detail.html', context)

@login_required(login_url='admin-login')
def createAppointmentView(request):
    form = AppointmentForm()
    if (request.method == 'POST'):
        form = AppointmentForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('appointment-list')
        else:
            messages.error(request, 'invalid form')

    context = {
        'form': form,
    }
    return render(request, 'adminapp/model_form.html', context)

@login_required(login_url='admin-login')
def editAppointmentView(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    form = AppointmentForm(instance=appointment)

    if (request.method == 'POST'):
        form = AppointmentForm(request.POST, request.FILES, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment-list')

    context = {
        'form': form,
    }

    return render(request, 'adminapp/model_form.html', context)

@login_required(login_url='admin-login')
def deleteAppointmentView(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    if(request.method == 'POST'):
        appointment.delete()
        return redirect('appointment-list')

    context = {
        'appointment': appointment,
    }
    return render(request, 'adminapp/delete_appointment.html', context)

#==========================================================
