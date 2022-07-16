from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('teachers/', TeacherPageView.as_view(), name='teachers'),
    path('students/', StudentPageView.as_view(), name='students'),

    path('export_students/', ExportToExcel.exportToExcelStudents, name='export_students'),
    path('export_teaches/', ExportToExcel.exportToExcelTeachers, name='export_teaches'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
] 
