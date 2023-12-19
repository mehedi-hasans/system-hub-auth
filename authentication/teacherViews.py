from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import Teacher, TeacherNotification

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