from django.urls import path
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
]
