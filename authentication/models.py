from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    USER = (
        (1, 'Admin'),
        (2, 'Teacher'),
        (3, 'Student'),
    )

    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')



#Course Create

class Course(models.Model):
    name= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class SessionYear(models.Model):
    session_start = models.CharField(max_length=100)
    session_end = models.CharField(max_length=100)

    def __str__(self):
        return self.session_start + '-' + self.session_end
    

class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address=models.TextField()
    gender = models.CharField(max_length=100)
    courseid = models.ForeignKey(Course, on_delete=models.DO_NOTHING,default=1)  # Set the default course
    sessionyearid = models.ForeignKey(SessionYear, on_delete=models.DO_NOTHING,default=1)
    cratedat = models.DateTimeField(auto_now_add=True)  # Set the default value using timezone.now
    updateat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    
class Teacher(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address=models.TextField()
    gender = models.CharField(max_length=100)
    mobile=models.CharField(max_length=100)
    courseid = models.ForeignKey(Course, on_delete=models.DO_NOTHING,default=2)
    experience=models.CharField(max_length=100)
    cratedat = models.DateTimeField(auto_now_add=True)  # Set the default value using timezone.now
    updateat = models.DateTimeField(auto_now=True)
       
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name



class Subject(models.Model):
    name=models.CharField(max_length=100)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    cratedat = models.DateTimeField(auto_now_add=True, null=True)  # Set the default value using timezone.now
    updateat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

#Teacher Panel
    
    
class TeacherNotification(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    status = models.IntegerField(null = True, default = 0)
    def __str__(self):
        return self.teacher_id.admin.first_name
    
class TeacherLeave(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    data = models.CharField(max_length=100)
    message =models.TextField()
    status = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.teacher_id.admin.first_name + self.teacher_id.admin.last_name
    
class StudentResult(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assignment_mark = models.IntegerField()
    exam_mark = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_id.admin.first_name