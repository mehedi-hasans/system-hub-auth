from django.shortcuts import render, redirect, HttpResponse
from .EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
#Profile Update
from .models import *
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


def changePassword(request):
    error_messages = {
        'success': 'Changed Successfully',
        'mismatch': 'New password and confirm password not matched',
        'old_password': 'Old password not match',
    }
    if request.method == "POST":
        old_password = request.POST.get("oldPassword")
        new_password = request.POST.get("newpassword")
        confirm_password = request.POST.get("confirmPassword")
        user = request.user
        if user.check_password(old_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, error_messages['success'])
                return redirect("loginPage")
            else:
                messages.error(request, error_messages['mismatch'])
        else:
            messages.error(request, error_messages['old_password'])
    return render(request, "changepassword.html")

def addStudent(request):
    error_messages = {
        'success': 'Student Add Successfully',
        'error': 'Student Add Failed',
    }
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")  # Changed from 'user_name' to 'username'
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("courseid")
        session_year_id = request.POST.get("sessionyearid")

        # Check if email or username already exists
        if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(username=username).exists():
            messages.error(request, error_messages['error'])
        else:
            # Create the customUser instance
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.profile_pic = profile_pic
            user.user_type = 3  # Assuming '3' represents students

            # Save the user instance
            user.save()

            # Retrieve the selected course and session year
            myCourse = Course.objects.get(id=course_id)
            mySessionYear = SessionYear.objects.get(id=session_year_id)

            # Create the student instance
            student = Student(
                admin=user,
                address=address,
                sessionyearid=mySessionYear,
                courseid=myCourse,
                gender=gender,
            )

            # Save the student instance
            student.save()

            messages.success(request, error_messages['success'])
            return redirect("addStudent")

    # Fetch the course and session year data to display in the form
    course = Course.objects.all()
    session_year = SessionYear.objects.all()
    context = {
        "course": course,
        "session": session_year, 
    }

    return render(request, "admin/addStudent.html", context)

def studentList(request):
    
    allStudent=Student.objects.all()
    print(allStudent)
    
    return render(request,"admin/studentList.html",{"student":allStudent})


def editStudent(request,id):
    student=Student.objects.filter(id=id)
    course = Course.objects.all()
    session_year = SessionYear.objects.all()
    context = {
        "course": course,
        "session": session_year,
        "student":student,
    }
    
    return render(request,"admin/editStudent.html",context)

def updateStudent(request):
    error_messages = {
        'success': 'Student Updated Successfully',
        'error': 'Student Updated Failed',
    }
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")  # Changed from 'user_name' to 'username'
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("courseid")
        session_year_id = request.POST.get("sessionyearid")
        print('This is ' + student_id + first_name)
        user=CustomUser.objects.get(id=student_id)
        
        user.first_name = first_name
        user.last_name = last_name
        user.email=email
        user.username=username
        
        if password is not None and password!="":
            user.set_password(password)
        if password is not None and profile_pic!="":
            user.profile_pic=profile_pic
        user.save()
        
        student=Student.objects.get(admin=student_id)
        student.address=address
        student.gender=gender
        
        course=Course.objects.get(id=course_id)
        student.courseid=course
        
        session=SessionYear.objects.get(id=session_year_id)
        student.sessionyearid=session
        
        student.save()
        
        messages.success(request, error_messages['success'])
        return redirect("studentList")
    
    return render(request,"admin/editStudent.html")


def deleteStudent(request,id):
    user=Student.objects.filter(id=id)
    user.delete()
    return redirect("studentList")



#Teacher Section
def addTeacher(request):
    error_messages = {
        'success': 'Teacher Add Successfully',
        'erroremail': 'email already exist',
        'errorusername': 'username already exist',
    }
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")  # Changed from 'user_name' to 'username'
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("courseid")
        mobile = request.POST.get("mobile")
        experience = request.POST.get("experience")

        # Check if email or username already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, error_messages['erroremail'])
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, error_messages['errorusername'])
        else:
            # Create the customUser instance
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.profile_pic = profile_pic
            user.user_type = 2  # Assuming '2' represents students

            # Save the user instance
            user.save()

            # Retrieve the selected course and session year
            myCourse = Course.objects.get(id=course_id)

            # Create the student instance
            teacher = Teacher(
                admin=user,
                address=address,
                courseid=myCourse,
                gender=gender,
                mobile=mobile,
                experience=experience,
            )

            # Save the student instance
            teacher.save()

            messages.success(request, error_messages['success'])
            return redirect("teacherList")

    # Fetch the course and session year data to display in the form
    course = Course.objects.all()
    context = {
        "course": course,
    }

    return render(request, "admin/addTeacher.html", context)


def teacherList(request):
    
    allTeacher=Teacher.objects.all()
    print(allTeacher)
    
    return render(request,"admin/teacherList.html",{"teacher":allTeacher})

def editTeacher(request,id):
    teacher=Teacher.objects.filter(id=id)
    course = Course.objects.all()
    context = {
        "course": course,
        "teacher":teacher,
    }
    
    return render(request,"admin/editTeacher.html",context)

def updateTeacher(request):
    
    error_messages = {
        'success': 'Teacher Updated Successfully',
        'error': 'Teacher update Failed',
    }
    if request.method == "POST":
        teacher_id = request.POST.get("teacher_id")
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username") 
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("courseid")
        mobile = request.POST.get("mobile")
        experience = request.POST.get("experience")
        
        user=CustomUser.objects.get(id=teacher_id)
        
        user.first_name = first_name
        user.last_name = last_name
        user.email=email
        user.username=username
        
        
        if password is not None and password!="":
            user.set_password(password)
        if password is not None and profile_pic!="":
            user.profile_pic=profile_pic
        user.save()
        
        teacher=Teacher.objects.get(admin=teacher_id)
        
        teacher.address=address
        teacher.gender=gender
        teacher.mobile=mobile
        teacher.experience=experience
        
        course=Course.objects.get(id=course_id)
        teacher.course_id=course
        
        teacher.save()
        
        
        messages.success(request, error_messages['success'])
        return redirect("teacherList")
    return render(request,"myAdmin/editTeacher.html")


def deleteTeacher(request,id):
    user=Teacher.objects.filter(id=id)
    user.delete()
    return redirect("teacherList")

