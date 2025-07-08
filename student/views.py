from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Student, Academic, Branch, Semester, Division, Course, Grade, Attendance, Assignment
from .forms import StudentLoginForm # You will create this form later

# --- Authentication Views (can be moved to a 'main' or 'accounts' app later) ---

def student_login_view(request):
    """
    Handles student login.
    After successful login, redirects to student dashboard.
    """
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Check if the user is associated with a Student profile
                # This assumes a OneToOneField from Student to User, which we haven't explicitly added yet,
                # but is a good practice for student logins. For now, we'll assume a direct User login.
                # You might verify if request.user is a student or teacher here.
                return redirect('student:dashboard')
            else:
                # Invalid login
                form.add_error(None, "Invalid username or password.")
    else:
        form = StudentLoginForm()
    return render(request, 'student/login.html', {'form': form})

@login_required
def student_logout_view(request):
    """
    Logs out the student and redirects to the main login page.
    """
    auth_logout(request)
    return redirect('main:home') # Redirect to your main app's home page (e.g., login choice)

# --- Student Dashboard and Information Views ---

@login_required
def student_dashboard(request):
    """
    Displays the student's main dashboard.
    Shows summary info and links to other student sections.
    """
    # Assuming the logged-in user is a student.
    # If Student model had a OneToOneField to User, you'd do:
    # student = get_object_or_404(Student, user=request.user)
    # For now, let's assume we fetch by some unique ID from the User or session,
    # or if we allow multiple Students per User for testing, just pick one.
    # For a real system, map the logged-in user to their Student profile.
    
    # Placeholder: Fetch a student, e.g., the first one for testing.
    # In a real app, you'd map request.user to a specific student object.
    try:
        student = Student.objects.first() # !!! Replace with actual logic to get *current* student !!!
        # Example: student = get_object_or_404(Student, user__username=request.user.username)
        # Or if Student has a OneToOneField 'user_account' to User:
        # student = get_object_or_404(Student, user_account=request.user)
    except Student.DoesNotExist:
        # Handle case where no student exists or logged-in user is not a student
        return render(request, 'student/no_student_profile.html') # Create this template

    context = {
        'student': student,
    }
    return render(request, 'student/dashboard.html', context)

@login_required
def student_profile(request):
    """
    Displays the detailed profile of the logged-in student.
    """
    try:
        student = Student.objects.first() # !!! Replace with actual logic to get *current* student !!!
    except Student.DoesNotExist:
        return render(request, 'student/no_student_profile.html')

    context = {
        'student': student,
    }
    return render(request, 'student/profile.html', context)

@login_required
def student_courses(request):
    """
    Lists the courses the student is enrolled in.
    """
    try:
        student = Student.objects.first() # !!! Replace with actual logic to get *current* student !!!
    except Student.DoesNotExist:
        return render(request, 'student/no_student_profile.html')

    # Get courses the student is enrolled in using the ManyToMany relationship
    enrolled_courses = student.enrolled_courses.all().select_related('branch', 'semester__academic') # Optimizing queries

    context = {
        'student': student,
        'enrolled_courses': enrolled_courses,
    }
    return render(request, 'student/courses.html', context)

@login_required
def student_grades(request):
    """
    Displays the grades for the student's courses.
    """
    try:
        student = Student.objects.first() # !!! Replace with actual logic to get *current* student !!!
    except Student.DoesNotExist:
        return render(request, 'student/no_student_profile.html')

    # Get all grades for this student, ordered by course and date if applicable
    grades = Grade.objects.filter(student=student).select_related('course').order_by('course__code')

    context = {
        'student': student,
        'grades': grades,
    }
    return render(request, 'student/grades.html', context)

@login_required
def student_attendance(request):
    """
    Displays the attendance records for the student.
    """
    try:
        student = Student.objects.first() # !!! Replace with actual logic to get *current* student !!!
    except Student.DoesNotExist:
        return render(request, 'student/no_student_profile.html')

    # Get all attendance records for this student, ordered by date and course
    attendance_records = Attendance.objects.filter(student=student).select_related('course').order_by('-date', 'course__code')

    context = {
        'student': student,
        'attendance_records': attendance_records,
    }
    return render(request, 'student/attendance.html', context)

@login_required
def student_assignments(request):
    """
    Lists all assignments for the student's enrolled courses.
    """
    try:
        student = Student.objects.first() # !!! Replace with actual logic to get *current* student !!!
    except Student.DoesNotExist:
        return render(request, 'student/no_student_profile.html')

    # Get assignments for all courses the student is enrolled in
    # This assumes Assignment has a ForeignKey to Course, and Course has ManyToMany to Student
    assigned_courses_ids = student.enrolled_courses.values_list('id', flat=True)
    assignments = Assignment.objects.filter(course__id__in=assigned_courses_ids).order_by('due_date')

    context = {
        'student': student,
        'assignments': assignments,
    }
    return render(request, 'student/assignments.html', context)
