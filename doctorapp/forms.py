from django.forms import ModelForm

from hospital.models import Appointment

class ManageAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('details', 'completed')