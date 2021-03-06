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
import datetime

from django.db.models import Q


from .forms import ManageAppointmentForm

# Create your views here.
#===============UTILITY==================
def is_admin(user):
    return user.groups.filter(name = 'Administrators').exists()

#=========================================

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def dashboardView(request):
    numpat=len(Patient.objects.all())
    numdoc=len(Doctor.objects.all())
    numapp=len(Appointment.objects.all().filter(completed=False))
    app=Appointment.objects.all().filter(date=datetime.datetime.today() )
    context={'numpat':numpat,'numdoc':numdoc,'numapp':numapp,'app':app,'page':"dash"}
    return render(request,'adminapp/dashboard.html',context)

def loginView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Current session has expired.")

    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(request,username=u,password=p)

        if user is not None:
            if not user.groups.filter(name = 'Administrators').exists():
                messages.error(request, "You are not an Admin")
                return redirect('index')

            login(request,user)
            messages.success(request, "Logged in successfully")
            return redirect('admin-dashboard')

        else:
            messages.error(request, 'Credentials do not match')
        
    context = {}
    return render(request,'adminapp/login.html',context)

def logoutView(request):
    logout(request)
    messages.info(request, "Logged Out")
    return redirect('admin-login')

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def manageAppointmentsList(request):
    requested_appointments = Appointment.objects.filter(completed=False).filter(confirmed=False)
    confirmed_appointments = Appointment.objects.filter(completed=False).filter(confirmed=True)
    context = {
        'requested_appointments': requested_appointments,
        'confirmed_appointments': confirmed_appointments,
    }
    return render(request, 'adminapp/manage_appointments_list.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def manageAppointment(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    form = ManageAppointmentForm(instance=appointment)

    if(request.method == 'POST'):
        form = ManageAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment saved")
            return redirect('manage-appointments-list')

    context = {
        'appointment': appointment,
        'form': form
    }
    return render(request, 'adminapp/manage_appointment.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def crudIndex(request):
    return render(request, 'adminapp/crud_index.html')

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def billListView(request):
    unpaid_bills = Bill.objects.filter(paid=False)
    paid_bills = Bill.objects.filter(paid=True)
    context = {
        'unpaid_bills': unpaid_bills,
        'paid_bills': paid_bills,
    }
    return render(request, 'adminapp/bill_list.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
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
        messages.success(request, "Bill created")
        return redirect('admin-bills')

    context = {
        'bill_items': bill_items,
    }
    return render(request, 'adminapp/generate_bill.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def billPdfView(request, id):
    bill = Bill.objects.get(pk=id)
    itemmap = bill.billitemmap_set.all()
    context = {
        'bill': bill,
        'itemmap': itemmap,
    }
    return render(request, 'adminapp/billpdf.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def billSetPaid(request, id):
    bill = get_object_or_404(Bill, pk = id)
    bill.paid = True
    bill.save()
    messages.success(request, "The bill has been set to paid.")
    return redirect('admin-bills')

#=================================================
#           BED MANAGEMENT
#=================================================

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def bedManagementList(request):

    occupied_no = Bed.objects.filter(occupied=True).count()
    occupied_beds = Bed.objects.filter(occupied=True)

    free_no = Bed.objects.filter(occupied=False).count()
    free_beds = Bed.objects.filter(occupied=False)

    context = {
        'occupied_no': occupied_no,
        'occupied_beds': occupied_beds,

        'free_no': free_no,
        'free_beds': free_beds,
    }

    return render(request, 'adminapp/beds_list.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def bedDetail(request, id):
    bed = get_object_or_404(Bed, pk=id)
    bedInstances = bed.bedinstance_set.all()
    context = {
        'bed': bed,
        'bedInstances': bedInstances,
    }
    return render(request, 'adminapp/bed_detail.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def bedAllot(request, id):
    bed = get_object_or_404(Bed, pk=id)
    if bed.occupied:
        messages.error(request, 'Bed already occupied')
        return redirect('bed-management-list')

    if request.method == 'POST':
        try:
            patient = Patient.objects.get(id=request.POST['patno'])
        except:
            messages.error(request, 'No such patient exists')
        else:
            if patient.admitted:
                messages.error(request, 'patient already admitted in other bed')
                return redirect('bed-management-list')

            BedInstance.objects.create(bed=bed, patient=patient)
            bed.occupied = True
            bed.save()
            patient.admitted = True
            patient.save()

            messages.success(request, "Bed Allotted")
            return redirect('bed-management-list')
            
    context = {
        'bed': bed,
    }
    return render(request, 'adminapp/bed_allot.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def bedDischarge(request, id):
    bed = get_object_or_404(Bed, pk=id)
    currentInstance = bed.currentInstance
    patient = currentInstance.patient
    if not bed.occupied:
        messages.error(request, 'Bed not occupied')
        return redirect('bed-management-list')

    if request.method == 'POST':
        bed.occupied = False
        bed.save()
        currentInstance.discharged = True
        currentInstance.discharged_on = datetime.datetime.now()
        currentInstance.save()
        patient.admitted = False
        patient.save()
        messages.success(request, 'Patient discharged from bed')
        return redirect('bed-management-list')

    context = {
        'bed': bed,
    }
    return render(request, 'adminapp/bed_discharge.html', context)

#=================================================
#           DOCTOR MODEL CRUD
#=================================================
@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def doctorListView(request):
    doctorList = Doctor.objects.all()
    context = {
        'list_of_doctors': doctorList,
    }
    return render(request, 'adminapp/doctor_list.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def doctorDetailView(request, id):
    doctor = get_object_or_404(Doctor, pk=id)
    context = {
        'doctor': doctor,
    }
    return render(request, 'adminapp/doctor_detail.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def createDoctorView(request):
    form = DoctorForm()
    if (request.method == 'POST'):
        form = DoctorForm(request.POST)
        if(form.is_valid()):
            form.save()
            doctor = form.instance
            doc_group = Group.objects.get_or_create(name='Doctors')[0]
            doc_group.user_set.add(doctor.user)
            doctor.user.save()
            messages.success(request, 'Data saved')
            return redirect('doctor-list')
        else:
            messages.error(request, 'Invalid form')

    context = {
        'form': form,
    }
    return render(request, 'adminapp/model_form.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def editDoctorView(request, id):
    doctor = get_object_or_404(Doctor, pk=id)
    form = DoctorForm(instance=doctor)

    if (request.method == 'POST'):
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data saved')
            return redirect('doctor-list')
        else:
            messages.error(request, 'Invalid form')

    context = {
        'form': form,
    }

    return render(request, 'adminapp/model_form.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def editPatientView(request, id):
    patient = get_object_or_404(Patient, pk=id)
    form = PatientForm(instance=patient)

    if (request.method == 'POST'):
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data saved')
            return redirect('patient-list')
        else:
            messages.error(request, 'Invalid form')

    context = {
        'form': form,
    }

    return render(request, 'adminapp/model_form.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def deleteDoctorView(request, id):
    doctor = get_object_or_404(Doctor, pk=id)
    if(request.method == 'POST'):
        doctor.delete()
        messages.info(request, "Data deleted.")
        return redirect('doctor-list')

    context = {
        'doctor': doctor,
    }
    return render(request, 'adminapp/delete_doctor.html', context)

#=================================================
#           PATIENT MODEL CRUD
#=================================================

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def patientListView(request):
    # Searching
    if request.GET.get('patid'):
        patid = int(request.GET.get('patid'))
        patientList = Patient.objects.filter(id=patid)

    elif request.GET.get('patname'):
        patientList = []
        patname = request.GET.get('patname')
        for patient in Patient.objects.all():
            if(patname.lower() in patient.name.lower()):
                patientList.append(patient)
    else:
        patientList = Patient.objects.all()


    context = {
        'list_of_patients': patientList,
    }
    return render(request, 'adminapp/patient_list.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def patientDetailView(request, id):
    patient = get_object_or_404(Patient, pk=id)
    appointments = patient.appointment_set.all()
    bedInstances = patient.bedinstance_set.all()
    context = {
        'patient': patient,
        'appointments': appointments,
        'bedInstances': bedInstances,
    }
    return render(request, 'adminapp/patient_detail.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def createPatientView(request):
    form = PatientForm()
    if (request.method == 'POST'):
        form = PatientForm(request.POST)
        if(form.is_valid()):
            form.save()
            patient = form.instance
            pat_group = Group.objects.get_or_create(name='Patients')[0]
            pat_group.user_set.add(patient.user)
            patient.user.save()
            messages.success(request, 'Data saved')
            return redirect('patient-list')
        else:
            messages.error(request, 'Invalid form')

    context = {
        'form': form,
    }
    return render(request, 'adminapp/model_form.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def editPatientView(request, id):
    patient = get_object_or_404(Patient, pk=id)
    form = PatientForm(instance=patient)

    if (request.method == 'POST'):
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data saved')
            return redirect('patient-list')
        else:
            messages.error(request, 'Invalid form')

    context = {
        'form': form,
    }

    return render(request, 'adminapp/model_form.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def deletePatientView(request, id):
    patient = get_object_or_404(Patient, pk=id)
    if(request.method == 'POST'):
        patient.delete()
        messages.info(request, 'Data deleted')
        return redirect('patient-list')

    context = {
        'patient': patient,
    }
    return render(request, 'adminapp/delete_patient.html', context)

#=================================================
#           APPOINTMENT MODEL CRUD
#=================================================

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def appointmentListView(request):
    appointmentList = Appointment.objects.all()
    context = {
        'list_of_appointments': appointmentList,
    }
    return render(request, 'adminapp/appointment_list.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def appointmentDetailView(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    context = {
        'appointment': appointment,
    }
    return render(request, 'adminapp/appointment_detail.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def createAppointmentView(request):
    form = AppointmentForm()
    if (request.method == 'POST'):
        form = AppointmentForm(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request, "Data saved")
            return redirect('appointment-list')
        else:
            messages.error(request, 'Invalid form')

    context = {
        'form': form,
    }
    return render(request, 'adminapp/model_form.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def editAppointmentView(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    form = AppointmentForm(instance=appointment)

    if (request.method == 'POST'):
        form = AppointmentForm(request.POST, request.FILES, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Data saved")
            return redirect('appointment-list')
        else:
            messages.error(request, 'Invalid form')

    context = {
        'form': form,
    }

    return render(request, 'adminapp/model_form.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin, login_url='admin-login')
def deleteAppointmentView(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    if(request.method == 'POST'):
        appointment.delete()
        messages.info(request, "Data deleted")
        return redirect('appointment-list')

    context = {
        'appointment': appointment,
    }
    return render(request, 'adminapp/delete_appointment.html', context)

#==========================================================
