from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

#-----------Teacher Panel----------------
@login_required
def teacherHome(request):
    return render(request, 'teacher/teacher.html')



