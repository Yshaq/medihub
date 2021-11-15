from django.forms import ModelForm, widgets
from hospital.models import Appointment, Bed, BedInstance
from django.contrib.admin.widgets import AdminTimeWidget, AdminDateWidget

class ManageAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('date', 'details', 'time', 'confirmed')
        widgets = {
            'date': widgets.DateInput(attrs={'type': 'date'}),
            'time': widgets.TimeInput(attrs={'type': 'time'}),
        }