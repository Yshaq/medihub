from django.shortcuts import get_object_or_404, render, redirect

from .models import Doctor, Patient, Appointment
from .forms import DoctorForm, PatientForm, AppointmentForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def landingPageView(request):
    return render(request, 'home.html')

def indexView(request):
    return render(request, 'hospital/index.html')

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

            doc_grp = Group.objects.get_or_create(name = 'Doctors-waiting')[0]
            doc_grp.user_set.add(user)
            user.save()

            doctor = Doctor.objects.create(user=user, first_name=first_name, last_name=last_name, gender=gender, dob=birthdate, department=department, phone=phonenumber, address=address, email=email)
            messages.success(request, "Doctor account created, waiting for approval.")
            return redirect('index')

        else:
            messages.error(request, "Passwords do not match")

    context = {'error' : error}
    return render(request, 'hospital/doctor_registration.html', context)


#=================================================
#           DOCTOR MODEL CRUD
#=================================================

def doctorListView(request):
    doctorList = Doctor.objects.all()
    context = {
        'list_of_doctors': doctorList,
    }
    return render(request, 'hospital/doctor_list.html', context)

def doctorDetailView(request, id):
    doctor = get_object_or_404(Doctor, pk=id)
    context = {
        'doctor': doctor,
    }
    return render(request, 'hospital/doctor_detail.html', context)

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
    return render(request, 'hospital/model_form.html', context)

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

    return render(request, 'hospital/model_form.html', context)

def deleteDoctorView(request, id):
    doctor = get_object_or_404(Doctor, pk=id)
    if(request.method == 'POST'):
        doctor.delete()
        return redirect('doctor-list')

    context = {
        'doctor': doctor,
    }
    return render(request, 'hospital/delete_doctor.html', context)

#=================================================
#           PATIENT MODEL CRUD
#=================================================

def patientListView(request):
    patientList = Patient.objects.all()
    context = {
        'list_of_patients': patientList,
    }
    return render(request, 'hospital/patient_list.html', context)

def patientDetailView(request, id):
    patient = get_object_or_404(Patient, pk=id)
    context = {
        'patient': patient,
    }
    return render(request, 'hospital/patient_detail.html', context)

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
    return render(request, 'hospital/model_form.html', context)

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

    return render(request, 'hospital/model_form.html', context)

def deletePatientView(request, id):
    patient = get_object_or_404(Patient, pk=id)
    if(request.method == 'POST'):
        patient.delete()
        return redirect('patient-list')

    context = {
        'patient': patient,
    }
    return render(request, 'hospital/delete_patient.html', context)

#=================================================
#           APPOINTMENT MODEL CRUD
#=================================================

def appointmentListView(request):
    appointmentList = Appointment.objects.all()
    context = {
        'list_of_appointments': appointmentList,
    }
    return render(request, 'hospital/appointment_list.html', context)

def appointmentDetailView(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    context = {
        'appointment': appointment,
    }
    return render(request, 'hospital/appointment_detail.html', context)

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
    return render(request, 'hospital/model_form.html', context)

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

    return render(request, 'hospital/model_form.html', context)

def deleteAppointmentView(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    if(request.method == 'POST'):
        appointment.delete()
        return redirect('appointment-list')

    context = {
        'appointment': appointment,
    }
    return render(request, 'hospital/delete_appointment.html', context)

#==========================================================
