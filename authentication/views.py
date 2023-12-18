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
    error_messages = {
        'password_error': 'Password invalid please try again!',
        'user_error': 'Username invalid please try again!',
    }
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('index')
            elif user_type == '2':
                return HttpResponse('This is Teacher Panel')
            else:
                return redirect('student')
        elif CustomUser.objects.filter(username=request.POST.get('username')).exists():
            messages.error(request, error_messages['password_error'])
            return redirect('loginPage')
        else:
            messages.error(request, error_messages['user_error'])
            return redirect('loginPage')
    return render(request, 'login.html')


def signupPage(request):
    error_messages = {
        'password_error': 'Password and Confirm Password not match',
        'user_error': 'Username already exists. Please choose a different username.',
        'email_error': 'Email already exists. Please choose a different Email.',
    }
    if request.method == "POST":
        uname = request.POST.get("name")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("confirmpassword")

        if CustomUser.objects.filter(username=uname).exists():
            messages.error(request, error_messages['user_error'])
            return redirect('signupPage')
        
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, error_messages['email_error'])
            return redirect('signupPage')
        
        elif pass1!= pass2:
            messages.error(request, error_messages['password_error'])
            return redirect('signupPage')
        
        else:
            # Use your customUser model to create a user
            myuser = CustomUser.objects.create_user(username=uname, email=email, password=pass1, user_type = 3)
            myuser.save()
            messages.success(request, 'Signup successful.')
            return redirect("loginPage")
    return render(request, "signup.html")

@login_required(login_url='/index')
def index(request):
    studentCount = Student.objects.all().count()
    teacherCount = Teacher.objects.all().count()
    departmentCount = Course.objects.all().count()
    subjectCount = Subject.objects.all().count()

    studentGenderMale = Student.objects.filter(gender = 'Male').count()
    studentGenderFemale = Student.objects.filter(gender = 'Female').count()

    context ={
        'studentCount' : studentCount,
        'teacherCount' : teacherCount,
        'departmentCount' : departmentCount,
        'subjectCount' : subjectCount,
        'studentGenderMale' : studentGenderMale,
        'studentGenderFemale' : studentGenderFemale,
    }
    return render(request, 'admin/admin.html', context)


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
            # cuser.profile_pic = profile_pic 
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

#Department Section
def addDepartment(request):
    
    error_messages = {
        'success': 'Department Add Successfully',
        'department_exist_error': 'Department already exist',
    }
    if request.method == "POST":
        department_name = request.POST.get("department_name")
        
        print(department_name)
        
        if Course.objects.filter(name=department_name):
            messages.error(request, error_messages['department_exist_error'])
        else:
            
            course=Course(
                
                name=department_name,
                
            )
            
            course.save()
            messages.success(request, error_messages['success'])
            
            return redirect("departmentList")
       
    return render(request,"admin/addDepartment.html")

def departmentList(request):
    
    department = Course.objects.all()
    context = {
        "department": department,
    }
    
    return render(request,"admin/departmentList.html",context)


def editDepartment(request,id):
    course = Course.objects.get(id=id)
    context = {
        "course": course,
    }
    return render(request,"admin/editDepartment.html",context)


def updateDepartment(request):
    error_messages = {
        'success': 'Department Updated Successfully',
        'error': 'Department Update Failed',
    }

    if request.method == "POST":
        department_id = request.POST.get("department_id")
        department_name = request.POST.get("department_name")
        
        course=Course.objects.get(id=department_id)
        course.name= department_name
        course.save()
        
        messages.success(request, error_messages['success'])
        return redirect("departmentList")
    else:
        messages.error(request, error_messages['error'])
        return redirect("editDepartment")
    
    return render(request,"admin/editDepartment.html")


def deleteDepartment(request,id):
    user=Course.objects.filter(id=id)
    user.delete()
    return redirect("departmentList")


#Subject Section
def addSubject(request):
    
    course=Course.objects.all()
    teacher=Teacher.objects.all()
    
    
    error_messages = {
        'success': 'Subject Add Successfully',
        'subjecterror': 'Subject already exist',
    }
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        teacher_id = request.POST.get("teacher_id")
        subject_name = request.POST.get("subject_name")
       
        courseid=Course.objects.get(id=course_id)
        teacherid=Teacher.objects.get(id=teacher_id)
    
        subject=Subject(
        
        name=subject_name,
        course=courseid,
        teacher=teacherid,
        )
        
        
    
        subject.save()
 
        messages.success(request, error_messages['success'])

        return redirect("subjectList")
    
    context={
        "course":course,
        "teacher":teacher,
        }    
    

    return render(request,"admin/addSubject.html", context)



def subjectList(request):
    subject = Subject.objects.all()
    context = {
        "subject": subject,
    }
    return render(request,"admin/subjectList.html",context)



def editSubject(request,id):
    subject=Subject.objects.filter(id=id)
    course=Course.objects.all()
    teacher=Teacher.objects.all()
    
    context={
        "subject":subject,
        "course":course,
        "teacher":teacher,
    }
    return render(request,"admin/editSubject.html",context)



def updateSubject(request):
    
    error_messages = {
        'success': 'Subject Update Successfully',
        'subjecterror': 'Subject Update Failed',
    }
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        course_id = request.POST.get("course_id")
        teacher_id = request.POST.get("teacher_id")
        subject_name = request.POST.get("subject_name")
       
        courseid=Course.objects.get(id=course_id)
        teacherid=Teacher.objects.get(id=teacher_id)
    
        subject=Subject(
        id=subject_id,
        name=subject_name,
        course=courseid,
        teacher=teacherid,
        )
        
        subject.save()
 
        messages.success(request, error_messages['success'])

        return redirect("subjectList")
    
    return render(request,"admin/editSubject.html")


def deleteSubject(request,id):
    user=Subject.objects.filter(id=id)
    user.delete()
    return redirect("subjectList")


@login_required(login_url='/index')
def student(request):
    return render(request, 'student/student.html')