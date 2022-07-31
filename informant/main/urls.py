from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    path('teachers/', TeacherPageView.as_view(), name='teachers'),
    path('teachers/<int:id>/', TeacherDetail.as_view(), name='teachers_detail'),
    path('teachers/add/', TeacherAddPageView.as_view(), name='teachers/add'),
    path('teacher/', Teacher.as_view(), name='teacher'),
    path('teacher/update/', Teacher.update, name='teacher_update'),
    path('teacher/delete/', Teacher.delete, name='teacher_delete'),

    path('students/', StudentPageView.as_view(), name='students'),
    path('students/<int:id>/', StudentDetail.as_view(), name='students_detail'),
    path('students/add/', StudentAddPageView.as_view(), name='students/add'),
    path('student/', Student.as_view(), name='student'),
    path('student/update/', Student.update, name='student_update'),
    path('student/delete/', Student.delete, name='student_delete'),

    path('export_students/', ExportToExcel.exportToExcelStudents, name='export_students'),
    path('export_teachers/', ExportToExcel.exportToExcelTeachers, name='export_teachers'),

    path('download_file_students/', DownloadFile.downloadFileStudents, name='download_file_students'),
    path('download_file_teachers/', DownloadFile.downloadFileTeachers, name='download_file_teachers'),

    path('kpk/', KpkView.as_view(), name='kpk'),
    path('kpk/update/', KpkView.update, name='kpk_update'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    path('reports/', ReportsPageView.as_view(), name='reports'),    
] 
