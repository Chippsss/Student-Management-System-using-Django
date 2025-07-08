from django.contrib import admin
from .models import Student, Academic, Branch, Semester, Division, Course, Grade, Attendance, Assignment

# Register your models for the admin interface
admin.site.register(Academic)
admin.site.register(Branch)
admin.site.register(Semester)
admin.site.register(Division)
admin.site.register(Course)
admin.site.register(Grade)
admin.site.register(Attendance)
admin.site.register(Assignment)

# You can customize the admin display for Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first', 'last', 'email', 'prn', 'division', 'academic', 'branch', 'semester')
    list_filter = ('academic', 'branch', 'semester', 'division')
    search_fields = ('id', 'first', 'last', 'email', 'prn')
    # You might want to prefetch related objects for performance in admin lists
    # raw_id_fields = ('academic_year', 'branch', 'current_semester', 'division') # Useful for many related objects
