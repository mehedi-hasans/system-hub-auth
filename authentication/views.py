from django.shortcuts import render, redirect, HttpResponse
from .EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
# Create your views here.
def loginPage(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user!=None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return HttpResponse('This is Admin Panel')
            elif user_type == '2':
                return HttpResponse('This is Teacher Panel')
            elif user_type == '3':
                return HttpResponse('This is Student Panel')
            else:
                messages.error(request, 'Email and Password are Invalid')
                return redirect('loginPage')
        else:
            messages.error(request, 'Email and Password are Invalid')
            return redirect('loginPage')
    return render(request, 'login.html')

def signupPage(request):
    return render(request, 'signup.html')

def index(request):
    return render(request, 'index.html')