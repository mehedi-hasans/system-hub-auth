from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import SessionYear, Student, StudentResult, Subject, Teacher, TeacherNotification

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
    teacher = Teacher.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(teacher_id=teacher)
    session_year = SessionYear.objects.all()

    action = request.GET.get('action')
    get_subject = None
    get_session = None
    students = None

    if action is not None and request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')

        get_subject = Subject.objects.get(id=subject_id)
        get_session = SessionYear.objects.get(id=session_year_id)

        students = Student.objects.filter(courseid=get_subject.course, sessionyearid=get_session)
        print(students)
    context = {
        'subjects': subjects,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session': get_session,
        'students': students,
    }

    return render(request, 'teacher/addResult.html', context)



def teacherSaveResult(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_mark = request.POST.get('assignment_mark')
        Exam_mark = request.POST.get('Exam_mark')
        print(f"subject_id: {subject_id}, student_id: {student_id}, assignment_mark: {assignment_mark}, Exam_mark: {Exam_mark}")


        get_student = Student.objects.get(admin = student_id)
        get_subject = Subject.objects.get(id=subject_id)

        check_exist = StudentResult.objects.filter(subject_id=get_subject, student_id=get_student).exists()
        if check_exist:
            result = StudentResult.objects.get(subject_id=get_subject, student_id=get_student)
            result.assignment_mark = assignment_mark
            result.exam_mark = Exam_mark
            result.save()
            messages.success(request, "Successfully Updated Result")
            return redirect('staff_add_result')
        else:
            result = StudentResult(student_id=get_student, subject_id=get_subject, exam_mark=Exam_mark,
                                   assignment_mark=assignment_mark)
            print(f"subject_id: {subject_id}, student_id: {student_id}, assignment_mark: {assignment_mark}, Exam_mark: {Exam_mark}")

            result.save()
            messages.success(request, "Successfully Added Result")
            return redirect('teacherSaveResult')