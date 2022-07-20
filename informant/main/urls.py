from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('teachers/', TeacherPageView.as_view(), name='teachers'),
    path('students/', StudentPageView.as_view(), name='students'),
    path('students/add/', StudentAddPageView.as_view(), name='students/add'),
    path('teachers/add/', TeacherAddPageView.as_view(), name='teachers/add'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
] 
