from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from student.models import Branch, Course, Academic, Semester, Division # Import models from student app

class Teacher(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='teacher_profile', help_text="Django User account associated with this teacher")
    employee_id = models.CharField(max_length=20,unique=True,help_text="Unique employee ID for the teacher")
    phone_number = models.CharField(max_length=15,blank=True,null=True,help_text="Teacher's contact phone number")
    
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL, null=True,blank=True,related_name='teachers',help_text="The academic branch this teacher belongs to")

    def __str__(self):
        full_name = self.user.get_full_name()
        return f"{full_name} ({self.employee_id})" if full_name else f"{self.user.username} ({self.employee_id})"

