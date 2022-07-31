from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('teachers/', TeacherPageView.as_view(), name='teachers'),
    path('teachers/add/', TeacherAddPageView.as_view(), name='teachers/add'),


    path('students/', StudentPageView.as_view(), name='students'),
    path('students/<int:id>/', StudentDetail.as_view(), name='students_detail'),
    path('students/add/', StudentAddPageView.as_view(), name='students/add'),

    path('export_students/', ExportToExcel.exportToExcelStudents, name='export_students'),
    path('export_teaches/', ExportToExcel.exportToExcelTeachers, name='export_teaches'),

    path('download_file_students/', DownloadFile.downloadFileStudents, name='download_file_students'),
    path('download_file_teachesr/', DownloadFile.downloadFileTeachers, name='download_file_teachesr'),

    path('student/', Student.as_view(), name='student'),
    path('teacher/', Teacher.as_view(), name='teacher'),

    path('kpk/', Kpk.as_view(), name='kpk'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
] 
