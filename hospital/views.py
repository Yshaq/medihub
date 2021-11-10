
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect


from .forms import DoctorForm, PatientForm, AppointmentForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def landingPageView(request):
	return redirect('index')

def indexView(request):
	return render(request, 'hospital/index.html')

def logoutView(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect('index')