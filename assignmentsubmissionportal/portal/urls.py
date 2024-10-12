from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .import views

urlpatterns = [
    path('student/register/',views.student_register,name="student-register"), #register new student
    path('student/login/',views.student_login,name="student-login"), #login student
    path('upload/',views.upload_assignment,name="assignment-Upload"), #upload assignments
    path('admins/',views.all_admins,name="admins"), #fetch all admins
    path('register/',views.admin_register,name="admin-register"), #admin register
    path('login/',views.admin_login,name="admin-login"), #admin login
    path('assignments/',views.assignment_show,name="admin-login"), #assignments tagged to particular admin
    path('assignments/<int:id>/accept',views.assignment_accept,name="admin-login"), #assignments accepted
    path('assignments/<int:id>/reject',views.assignment_reject,name="admin-login"), #assignments rejected
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)