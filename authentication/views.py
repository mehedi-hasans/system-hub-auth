from django.shortcuts import render

# Create your views here.
def loginPage(request):
    return render(request, 'login.html')

def signupPage(request):
    return render(request, 'signup.html')

def index(request):
    return render(request, 'index.html')