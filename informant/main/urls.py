from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('teachers/', TeacherPageView.as_view(), name='teachers'),
    path('students/', StudentPageView.as_view(), name='students'),
    path('students/add/', StudentAddPageView.as_view(), name='students/add'),
    path('teachers/add/', TeacherAddPageView.as_view(), name='teachers/add'),

    path('export_students/', ExportToExcel.exportToExcelStudents, name='export_students'),
    path('export_teaches/', ExportToExcel.exportToExcelTeachers, name='export_teaches'),

    path('download_file_students/', DownloadFile.downloadFileStudents, name='download_file_students'),
    path('download_file_teaches/', DownloadFile.downloadFileTeachers, name='download_file_teaches'),

    path('student/', Student.as_view(), name='student'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
] 
