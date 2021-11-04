from django.forms import ModelForm
from .models import Doctor, Patient, Appointment

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'