from django.forms import ModelForm
from .models import Doctor, Patient, Appointment

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'