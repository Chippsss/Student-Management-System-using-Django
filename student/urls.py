from django.urls import path

from . import views

app_name = "student"

urlpatterns = [
    # Authentication URLs
    path('login/', views.student_login_view, name='login'),
    path('logout/', views.student_logout_view, name='logout'),

    # Student Dashboard and Info
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('profile/', views.student_profile, name='profile'),
    path('courses/', views.student_courses, name='courses'),
    path('grades/', views.student_grades, name='grades'),
    path('attendance/', views.student_attendance, name='attendance'),
    path('assignments/', views.student_assignments, name='assignments'),
]
