from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    patients = models.ManyToManyField('Patient')
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(max_length=400, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    salary_in_rs = models.IntegerField(null=True, blank=True)
    schedule = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.department}'

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(max_length=400, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.id}'

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    details = models.TextField(max_length=1000, null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.doctor} with {self.patient} on {self.date}'

    class Meta:
        ordering = ['-date', 'time']

class Bill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} Rs.{self.total}"

class Item(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} Rs.{self.price}'

class BillItemMap(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    qty = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.bill.id} - {self.item.name}'

    @property
    def subtotal(self):
        return (self.item.price * self.qty)