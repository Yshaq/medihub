from django.forms import ModelForm
from .models import Doctor, Patient, Appointment
from django import forms
from django.forms import widgets

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'date': widgets.DateInput(attrs={'type': 'date'}),
            'time': widgets.TimeInput(attrs={'type': 'time'}),
        }