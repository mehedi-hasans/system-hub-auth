from django.urls import path

from authentication import teacherViews
from . import views

urlpatterns = [
    path('', views.loginPage, name='loginPage'),
    path('signup', views.signupPage, name='signupPage'),
    path('index', views.index, name='index'),
    path('logOut', views.logOut, name='logOut'),
    #Profile Update
    path('profile', views.profile, name='profile'),
    path('profile/update', views.profileUpdate, name='profileUpdate'),
    path('profile/profileUpdate/ChangePassword', views.changePassword,name="changePassword"),
    #Student
    path('addStudent', views.addStudent, name='addStudent'),
    path('myAdmin/Student/studentList', views.studentList,name="studentList"), 
    path('myAdmin/Student/editStudent/<str:id>', views.editStudent,name="editStudent"),
    path('myAdmin/Student/updateStudent', views.updateStudent,name="updateStudent"),
    path('myAdmin/Student/deleteStudent/<str:id>', views.deleteStudent,name="deleteStudent"),
    #Teacher
    path('myAdmin/addTeacher', views.addTeacher,name="addTeacher"), 
    path('myAdmin/Teacher/teacherList', views.teacherList,name="teacherList"), 
    path('myAdmin/Teacher/editTeacher/<str:id>', views.editTeacher, name="editTeacher"),
    path('myAdmin/Teacher/updateTeacher', views.updateTeacher,name="updateTeacher"), 
    path('myAdmin/Teacher/deleteTeacher/<str:id>', views.deleteTeacher,name="deleteTeacher"),
    #Department
    path('myAdmin/addDepartment', views.addDepartment,name="addDepartment"),
    path('myAdmin/departmentList', views.departmentList,name="departmentList"),
    path('myAdmin/editDepartment/<str:id>', views.editDepartment,name="editDepartment"), 
    path('myAdmin/updateDepartment', views.updateDepartment,name="updateDepartment"), 
    path('myAdmin/deleteDepartment/<str:id>', views.deleteDepartment,name="deleteDepartment"), 
    #Subject
    path('myAdmin/Subject/addSubject', views.addSubject,name="addSubject"), 
    path('myAdmin/Subject/subjectList', views.subjectList,name="subjectList"), 
    path('myAdmin/Subject/editSubject/<str:id>', views.editSubject,name="editSubject"), 
    path('myAdmin/Subject/updateSubject', views.updateSubject,name="updateSubject"),
    path('myAdmin/Subject/deleteSubject/<str:id>', views.deleteSubject,name="deleteSubject"),

    #Teacher Panel
    path('teacher/home', teacherViews.teacherHome, name='teacherHome'),
    path('teacher/send_notification', teacherViews.TeacherSendNotification, name='TeacherSendNotification'),
    path('teacher/save_teacher_notification', teacherViews.saveTeacherNotification, name='saveTeacherNotification'),
    path('teacher/notification', teacherViews.notification, name='notification'),
    path('teacher/teacherNoMarkAsDone/<str:status>', teacherViews.teacherNoMarkAsDone, name='teacherNoMarkAsDone'),

    path('teacher/add/result', teacherViews.teacherAddResult, name='teacherAddResult'),



    #Student Panel
    path('student', views.studentHome, name='student'),
]
