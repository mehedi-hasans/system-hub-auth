from django.shortcuts import render, redirect, HttpResponse
from .EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
#Profile Update
from .models import CustomUser
# Create your views here.
def loginPage(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user!=None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('index')
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

@login_required(login_url='/')
def index(request):
    return render(request, 'admin/admin.html')



def logOut(request):
    logout(request)
    return redirect('loginPage')

#Profile Update Section
@login_required(login_url='/')
def profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/')
def profileUpdate(request):
    error_messages = {
        'success': 'Profile Update Successfully',
        'error': 'Profile Not Updated',
        'password_error': 'Current password is incorrect',
    }
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        password = request.POST.get("password")
        username = request.POST.get("username")
        email = request.POST.get("email")
        try:
            cuser = CustomUser.objects.get(id=request.user.id)
            cuser.first_name = firstname
            cuser.last_name = lastname
            cuser.profile_pic = profile_pic
            # Verify the current password provided matches the user's current password
            if not cuser.check_password(password):
                messages.error(request, error_messages['password_error'])
            else:
                # If the current password is correct, proceed to update other fields
                if profile_pic is not None:
                    cuser.profile_pic = profile_pic
                
                # You can add additional fields to update here as needed

                cuser.save()
                auth_login(request, cuser)
                messages.success(request, error_messages['success'])
                return redirect("profileUpdate")
        except:
            messages.error(request, error_messages['error'])
    return render(request, 'profile.html')