from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)

admin.site.register(Bill)
admin.site.register(Item)
admin.site.register(BillItemMap)
admin.site.register(Bed)
admin.site.register(BedInstance)