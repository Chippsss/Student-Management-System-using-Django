from django.urls import path
from . import views

app_name = "teacher" # IMPORTANT: Define the app namespace

urlpatterns = [
    # Authentication URLs
    path('login/', views.teacher_login_view, name='login'),
    path('logout/', views.teacher_logout_view, name='logout'),

    # Teacher Dashboard and Course Management
    path('dashboard/', views.teacher_dashboard, name='dashboard'),
    path('course/<int:course_id>/', views.teacher_course_detail, name='course_detail'),
    path('course/<int:course_id>/attendance/', views.teacher_manage_attendance, name='manage_attendance'),
    path('course/<int:course_id>/grades/', views.teacher_manage_grades, name='manage_grades'),
    path('course/<int:course_id>/assignments/', views.teacher_manage_assignments, name='manage_assignments'),
]