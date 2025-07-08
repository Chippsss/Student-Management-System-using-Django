
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from student.models import Student 
from teacher.models import Teacher 


def home_view(request):
    
    if request.user.is_authenticated:
        
        if hasattr(request.user, 'teacher_profile'):
            return redirect('teacher:dashboard')
        
        
        elif hasattr(request.user, 'student_profile'):
            return redirect('student:dashboard')
        
        else:
           
            return render(request, 'main/select_role.html', {
                'message': 'Your account is logged in, but no specific student or teacher profile is linked. Please contact support or complete your profile setup.',
                'user': request.user
            })
    
    
    return render(request, 'main/home.html')