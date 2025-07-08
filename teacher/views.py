from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Teacher # Import your Teacher model
from student.models import Course, Student, Grade, Attendance, Assignment, Division # Import models from student app
from .forms import TeacherLoginForm # You will create this form later

# --- Authentication Views for Teachers ---

def teacher_login_view(request):
    """
    Handles teacher login.
    After successful login, redirects to teacher dashboard.
    """
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Ensure the user has a linked Teacher profile
                try:
                    teacher_profile = Teacher.objects.get(user=user)
                    auth_login(request, user)
                    return redirect('teacher:dashboard')
                except Teacher.DoesNotExist:
                    form.add_error(None, "No teacher profile found for this user.")
            else:
                # Invalid login
                form.add_error(None, "Invalid username or password.")
    else:
        form = TeacherLoginForm()
    return render(request, 'teacher/login.html', {'form': form})

@login_required
def teacher_logout_view(request):
    """
    Logs out the teacher and redirects to the main login page.
    """
    auth_logout(request)
    return redirect('main:home') # Redirect to your main app's home page

# --- Teacher Dashboard and Functionality Views ---

@login_required
def teacher_dashboard(request):
    """
    Displays the teacher's main dashboard.
    Shows assigned courses and quick links for management.
    """
    teacher_profile = get_object_or_404(Teacher, user=request.user)
    assigned_courses = teacher_profile.courses_taught.all().select_related('branch', 'semester__academic_year')

    context = {
        'teacher': teacher_profile,
        'assigned_courses': assigned_courses,
    }
    return render(request, 'teacher/dashboard.html', context)

@login_required
def teacher_course_detail(request, course_id):
    """
    Displays details for a specific course taught by the teacher.
    Allows viewing students, grades, attendance, assignments for that course.
    """
    teacher_profile = get_object_or_404(Teacher, user=request.user)
    # Ensure the logged-in teacher is assigned to this course
    course = get_object_or_404(Course, id=course_id, teacher=teacher_profile)

    # Get students enrolled in this course (can filter by division later if needed)
    enrolled_students = course.students_enrolled.all().select_related('branch', 'current_semester', 'division').order_by('last', 'first')

    context = {
        'teacher': teacher_profile,
        'course': course,
        'enrolled_students': enrolled_students,
        # You'll add forms for taking attendance, entering grades, etc. here
    }
    return render(request, 'teacher/course_detail.html', context)

@login_required
def teacher_manage_attendance(request, course_id):
    """
    Allows the teacher to view and manage attendance for a specific course.
    Includes filtering by division and date.
    """
    teacher_profile = get_object_or_404(Teacher, user=request.user)
    course = get_object_or_404(Course, id=course_id, teacher=teacher_profile)

    # Get distinct divisions associated with students enrolled in this course
    # This ensures we only show divisions that actually have students in this course
    available_divisions = Division.objects.filter(
        students_in_division__enrolled_courses=course
    ).distinct().order_by('name')

    selected_division = None
    selected_date = None
    attendance_records = []
    students_in_selected_division = []

    if request.method == 'POST':
        # Handle form submission for saving attendance
        # This part would involve processing a form (e.g., ModelFormSet)
        # to update/create Attendance records.
        # For simplicity, we'll just demonstrate fetching below.
        pass

    # Filtering logic for GET requests
    if 'division' in request.GET and request.GET['division']:
        selected_division = get_object_or_404(Division, id=request.GET['division'])
        students_in_selected_division = Student.objects.filter(
            division=selected_division,
            enrolled_courses=course # Filter for students in this course and division
        ).order_by('last', 'first')

        if 'date' in request.GET and request.GET['date']:
            try:
                selected_date = request.GET['date']
                # Convert date string to date object
                from datetime import datetime
                date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()

                # Fetch existing attendance for this course, division, and date
                attendance_records = Attendance.objects.filter(
                    course=course,
                    student__division=selected_division,
                    date=date_obj
                ).select_related('student', 'student__division').order_by('student__last')

                # Create a set of student IDs who already have attendance recorded for this day
                recorded_student_ids = {rec.student.id for rec in attendance_records}

                # For students without an attendance record for this date, assume absent or create a default
                # This logic is more complex and usually handled by a formset in a real app
                # For display, we can show all students and if they have a record
                students_with_attendance_status = []
                for student in students_in_selected_division:
                    status = None
                    record_exists = False
                    for record in attendance_records:
                        if record.student == student:
                            status = record.is_present
                            record_exists = True
                            break
                    students_with_attendance_status.append({
                        'student': student,
                        'is_present': status, # True/False/None
                        'record_exists': record_exists,
                    })
                students_in_selected_division = students_with_attendance_status

            except ValueError:
                # Handle invalid date format
                selected_date = None
    
    context = {
        'teacher': teacher_profile,
        'course': course,
        'available_divisions': available_divisions,
        'selected_division': selected_division,
        'selected_date': selected_date,
        'students_in_division': students_in_selected_division, # List of students with their attendance status
        'attendance_records': attendance_records, # Raw attendance records for reference
    }
    return render(request, 'teacher/manage_attendance.html', context)

@login_required
def teacher_manage_grades(request, course_id):
    """
    Allows the teacher to view and manage grades for a specific course.
    """
    teacher_profile = get_object_or_404(Teacher, user=request.user)
    course = get_object_or_404(Course, id=course_id, teacher=teacher_profile)

    # Get grades for students in this course
    grades = Grade.objects.filter(course=course).select_related('student', 'student__division').order_by('student__last', 'student__first')

    context = {
        'teacher': teacher_profile,
        'course': course,
        'grades': grades,
    }
    return render(request, 'teacher/manage_grades.html', context)

@login_required
def teacher_manage_assignments(request, course_id):
    """
    Allows the teacher to view, create, and manage assignments for a specific course.
    """
    teacher_profile = get_object_or_404(Teacher, user=request.user)
    course = get_object_or_404(Course, id=course_id, teacher=teacher_profile)

    assignments = Assignment.objects.filter(course=course).order_by('due_date')

    context = {
        'teacher': teacher_profile,
        'course': course,
        'assignments': assignments,
    }
    return render(request, 'teacher/manage_assignments.html', context)