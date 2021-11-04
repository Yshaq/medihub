
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect


from .forms import DoctorForm, PatientForm
from django.contrib import messages

# Create your views here.
def landingPageView(request):
	return render(request, 'home.html')

def indexView(request):
	return render(request, 'hospital/index.html')
def loginpage(request):
	error = ""
	page = ""
	if request.method == 'POST':
		u = request.POST['username']
		p = request.POST['password']
		user = authenticate(request,username=u,password=p)
		render(request,'hospital/patientdashboard.html')
		try:
			if user is not None:
				login(request,user)
				error = "no"
				g = request.user.groups.all()[0].name
				
				if g == 'Patients':
					page = "patient"
					d = {'error': error,'page':page}
					return render(request,'hospital/patientdashboard.html',d)
			else:
				error = "yes"
		except Exception as e:
			error = "yes"
			print(e)
			raise e
	context = {'error': error}
	print(error)
	return render(request,'hospital/login.html',context)


def PatientRegisteration(request):
	error = ""
	user="none"
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		password = request.POST['password']
		repeatpassword = request.POST['repeatpassword']
		gender = request.POST['gender']
		phonenumber = request.POST['phonenumber']
		address = request.POST['address']
		birthdate = request.POST['dateofbirth']
		
		try:
			if password == repeatpassword:
				Patient.objects.create(first_name=first_name,last_name=last_name,email=email,password=password,gender=gender,phone=phonenumber,address=address,dob=birthdate)
				user = User.objects.create_user(first_name=first_name,email=email,username=email)
				pat_group = Group.objects.get(name='Patients')
				pat_group.user_set.add(user)
				#print(pat_group)
				user.save()
				#print(user)
				error = "no"
			else:
				error = "yes"
		except Exception as e:
			error = "yes"
			print("Error:",e)
	context = {'error' : error}
	#print(error)
	return render(request,'hospital/patientregistration.html',context)

			
def Login_admin(request):
	error = ""
	if request.method == 'POST':
		u = request.POST['username']
		p = request.POST['password']
		user = authenticate(username=u,password=p)
		try:
			if user.is_staff:
				login(request,user)
				error = "no"
			else:
				error = "yes"
		except:
			error = "yes"
	d = {'error' : error}
	return render(request,'hospital/AdminLogin.html',d)


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
def AdminHome(request):
	#after login user comes to this page.
	if not request.user.is_staff:
		return redirect('login_admin')
	return render(request,'hospital/admindashboard.html')

def Logout_admin(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	logout(request)
	return redirect('login_admin')