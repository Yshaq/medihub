
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.utils import timezone

# Create your views here.
def landingPageView(request):
    return render(request, 'home.html')

def indexView(request):
    return render(request, 'hospital/index.html')
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
	return render(request,'login.html',d)