from django.shortcuts import render

# Create your views here.
def landingPageView(request):
    return render(request, 'home.html')

def indexView(request):
    return render(request, 'hospital/index.html')
