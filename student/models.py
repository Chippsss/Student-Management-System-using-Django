from django.db import models
from django.contrib.auth.models import User # Import Django's built-in User model


# Create your models here.

class Academic(models.Model):
    year = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.year}"
###########################################################################################   

class Semester(models.Model):
    FIRST = '1st'
    SECOND = '2nd'
    THIRD = '3rd'
    FOURTH = '4th'
    FIFTH = '5th'
    SIXTH = '6th'
    SEVENTH = '7th'
    EIGHTH = '8th'

    SEMESTER_NUMBER_CHOICES = [
        (FIRST, 'Semester 1'),
        (SECOND, 'Semester 2'),
        (THIRD, 'Semester 3'),
        (FOURTH, 'Semester 4'),
        (FIFTH, 'Semester 5'),
        (SIXTH, 'Semester 6'),
        (SEVENTH, 'Semester 7'),
        (EIGHTH, 'Semester 8'),
    ]

    semester_number = models.CharField(
        max_length=5,
        choices=SEMESTER_NUMBER_CHOICES,
        help_text="e.g., 1st, 2nd, 3rd, 4th, 5th, 6th, 7th, 8th"
    )
    
    # Link to the AcademicYear this semester belongs to
    academic = models.ForeignKey(Academic, on_delete=models.CASCADE, related_name='semesters', help_text="Academic year this semester belongs to")

    def __str__(self):
        return f"{self.semester_number} ({self.academic.year})"
##############################################################################################

class Branch(models.Model):
    name = models.CharField(max_length=50, unique=True) 
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f"{self.code}: {self.name}"
###########################################################################################       

class Division(models.Model):
    """Represents a specific division within a branch for a given academic year."""
    name = models.CharField(max_length=10, help_text="e.g., A, B, C, D") # 'A', 'B', etc.
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,related_name='divisions',help_text="The branch this division belongs to")
    academic = models.ForeignKey(Academic, on_delete=models.CASCADE, related_name='divisions_in_year', help_text="The academic year this division is for")

    def __str__(self):
        return f"{self.name}"
#################################################################################################

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,related_name='student_profile',help_text="User account associated with this student for login")
    id = models.CharField(max_length=15, primary_key=True)
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    email = models.EmailField(default=None)
    prn = models.BigIntegerField(default=None)
    # academic = models.CharField(max_length=15, null=True, choices=YEAR_CHOICES, help_text="Choose Your current year")
    # branch = models.CharField(max_length=50, null=True, choices=BRANCH_CHOICES, help_text="Choose your branch")
    
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True, related_name='students_in_division', help_text="The student's assigned division")
    
    academic = models.ForeignKey(Academic, on_delete=models.SET_NULL, null=True, blank=True, related_name="students_in_year", help_text="Choose the student's current academic year")
    
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="students_in_branch", help_text="choose the student's branch")
    
    semester = models.ForeignKey(Semester,on_delete=models.SET_NULL,null=True,blank=True,related_name='students_in_semester',help_text="The student's current academic semester")
    
    def __str__(self):
        return (f"{self.id}: {self.first} {self.last} {self.prn} {self.division} {self.academic} {self.branch} {self.semester}")
###########################################################################################   
    
    
class Course(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="courses")
    academic = models.ForeignKey(Academic, on_delete=models.CASCADE, related_name="courses_offered")
    students_enrolled = models.ManyToManyField(Student, related_name="enrolled_courses", blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses_offered', help_text="The semester in which this course is typically offered")
    
    def __str__(self):
        return f"{self.code} - {self.name} ({self.branch.name}, {self.academic.year})"
###############################################################################################
    
    
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades_received')
    score = models.DecimalField(max_digits=5, decimal_places=2) # e.g., 85.50
    grade_letter = models.CharField(max_length=5, blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.first} {self.student.last} - {self.course.code}: {self.score}"

###############################################################################################

class Attendance(models.Model):
    """Records attendance for a student in a course on a specific date."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_taken')
    date = models.DateField()
    is_present = models.BooleanField(default=True)

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.first} {self.student.last} - {self.course.code} on {self.date}: {status}"

    
class Assignment(models.Model):
    """Represents an assignment for a course."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    due_date = models.DateTimeField()
    max_score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.title} ({self.course.code})"