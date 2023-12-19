from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import SessionYear, Student, Subject, Teacher, TeacherNotification

#-----------Teacher Panel----------------
@login_required
def teacherHome(request):
    return render(request, 'teacher/teacher.html')


def TeacherSendNotification(request):
    allTeacher = Teacher.objects.all()
    notification = TeacherNotification.objects.all()
    context = {
        'teacher': allTeacher,
        'notification' : notification
    }
    return render(request, 'admin/teacherNotification.html', context)


def saveTeacherNotification(request):
    if request.method =='POST':
        teacherId = request.POST.get('teacher_id')
        message = request.POST.get('message')
        print(message, teacherId)
        teacher = Teacher.objects.get(admin = teacherId)
        notification = TeacherNotification(
            teacher_id = teacher,
            message = message
        )
        notification.save()
        messages.success(request, 'Send Notification Success')
        return redirect('TeacherSendNotification')
    else:
        messages.error(request, 'Send Notification Do not save!')
        return redirect('TeacherSendNotification')
    

def notification(request):
    teacher = Teacher.objects.filter(admin = request.user.id)
    for i in teacher:
        teacherId = i.id
        notification = TeacherNotification.objects.filter(teacher_id = teacherId)
        context ={
            'notification' : notification
        }
    return render(request, 'teacher/notification.html', context)


def teacherNoMarkAsDone(request, status):
    notification = TeacherNotification.objects.get(id = status)
    notification.status = 1
    notification.save()

    return redirect('notification')


def teacherAddResult(request):
    teacher = Teacher.objects.get(admin = request.user.id)

    subjects = Subject.objects.filter(teacher_id = teacher)
    session_year = SessionYear.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session = None
    students = None
    if action is not None:
        if request.method == "POST":
           subject_id = request.POST.get('subject_id')
           session_year_id = request.POST.get('session_year_id')

           get_subject = Subject.objects.get(id = subject_id)
           get_session = SessionYear.objects.get(id = session_year_id)

           subjects = Subject.objects.filter(id = subject_id)
           for i in subjects:
               student_id = i.id
               students = Student.objects.filter(courseid = student_id)


    context = {
        'subjects':subjects,
        'session_year':session_year,
        'action':action,
        'get_subject':get_subject,
        'get_session':get_session,
        'students':students,
    }

    return render(request, 'teacher/addResult.html', context)