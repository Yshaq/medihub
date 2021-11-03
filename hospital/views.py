from django.shortcuts import get_object_or_404, render, redirect

from hospital.models import Doctor
from .forms import DoctorForm
from django.contrib import messages

# Create your views here.
def landingPageView(request):
    return render(request, 'home.html')

def indexView(request):
    return render(request, 'hospital/index.html')

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
    return render(request, 'hospital/doctor_form.html', context)

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

    return render(request, 'hospital/doctor_form.html', context)

def deleteDoctorView(request, id):
    doctor = get_object_or_404(Doctor, pk=id)
    if(request.method == 'POST'):
        doctor.delete()
        return redirect('doctor-list')

    context = {
        'doctor': doctor,
    }
    return render(request, 'hospital/delete_doctor.html', context)
