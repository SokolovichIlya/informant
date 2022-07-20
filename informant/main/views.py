from urllib import response
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView, View

from django.db.models import *

from .forms import LoginForm, StudentsForm


from .models import Students

import datetime
import json

def customDateSerialize(o):
    if isinstance(o, datetime.date):
        return o.__str__()

class HomePageView(TemplateView):
    template_name = "pages/home.html"

class TeacherPageView(TemplateView):
    template_name = "pages/teachers/list.html"

class StudentPageView(TemplateView):
    template_name = "pages/students/list.html"

class StudentAddPageView(TemplateView):
    template_name = "pages/students/add.html"

class TeacherAddPageView(TemplateView):
    template_name = "pages/teachers/add.html"

    def get_context_data(self, **kwargs):
        context = {'form': StudentsForm}

        return context


class Student(View):
    def get(self, request):
        try:
            fio = request.data.get('fio') or None
            page = request.data.get('page') or 1
            per_page = 10 # лимит отображения на странице
            

            data = Students.objects.filter(fio=fio).values()

            total = data.count()


            if total%per_page != 0:
                total_page = total//per_page+1
            else:
                total_page = total / per_page
            
            students = {
                'data':data,
                'total': total,
                'per_page': per_page,
                'page': page,
                'total_page': total_page,
            }

            return JsonResponse(data=students, safe=False)
        
        except Exception as e:
            return response(e)
    
    def post(self, request):
        try:
            fio = request.data.get('fio')
            participation_period = request.data.get('participation_period')
            mounth = request.data.get('mounth')
            level  = request.data.get('level')
            category  = request.data.get('category')
            document = request.data.get('document')
            teacher  = request.data.get('teacher')
            participation_in_profile_shifts = request.data.get('participation_in_profile_shifts')
            name_program = request.data.get('name_program')

            Students.objects.create(fio, participation_period, mounth, level, category, document, teacher, 
                                                participation_in_profile_shifts, name_program)


            return HttpResponse(status_code=200)

        except Exception as e:
            return response(e)

    def put(self, request):
        try:
            student_id = request.data.get('student_id')
            fio = request.data.get('fio')
            participation_period = request.data.get('participation_period')
            mounth = request.data.get('mounth')
            level  = request.data.get('level')
            category  = request.data.get('category')
            document = request.data.get('document')
            teacher  = request.data.get('teacher')
            participation_in_profile_shifts = request.data.get('participation_in_profile_shifts')
            name_program = request.data.get('name_program')


            Students.objects.filter(id=student_id).update(fio=fio, participation_period=participation_period, 
                                                            mounth=mounth, level=level, category=category, 
                                                            document=document, teacher=teacher, 
                                                            participation_in_profile_shifts=participation_in_profile_shifts,
                                                            name_program=name_program)

            return HttpResponse(status_code=200)
        
        except Exception as e:
            return response(e)

    def delete(self, request):
        try:
            student_id = request.data.get('student_id')

            student = Students.objects.get(id=student_id)
            student.delete()

            return HttpResponse(status_code=200)
        
        except Exception as e:
            return response(e)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse(status_code=200)
                else:
                    return HttpResponse(status_code=401)
            else:
                return HttpResponse(status_code=403)
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def logout( request):
    logout(request)
    return redirect('/')

