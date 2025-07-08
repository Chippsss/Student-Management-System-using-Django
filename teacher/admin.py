from django.contrib import admin
from .models import Teacher

# You can customize the admin display for Teacher
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'branch', 'phone_number')
    list_filter = ('branch',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id')
    raw_id_fields = ('user', 'branch') # Use raw_id_fields for ForeignKey to User for better UI
