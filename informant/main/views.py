from urllib import response
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView, View

from django.db.models import *
from django.db.models.functions import Lower

from .forms import LoginForm, StudentsForm, TeachersForm


from .models import Students, Teachers

import datetime
import json

import xlwt

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
            fio = request.GET('fio') or None
            page = request.GET('page')
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
            form = StudentsForm(request.POST, request.FILES)

            fio = request.POST('fio')
            participation_period = request.POST('participation_period')
            mounth = request.POST('mounth')
            level  = request.POST('level')
            category  = request.POST('category')
            document = request.FILES['document']
            teacher  = request.POST('teacher')
            result  = request.POST('result')
            participation_in_profile_shifts = request.POST('participation_in_profile_shifts')
            name_program = request.POST('name_program')

            Students.objects.create(fio, participation_period, mounth, level, category, document, teacher, 
                                    result, participation_in_profile_shifts, name_program)


            return HttpResponse(status_code=200)

        except Exception as e:
            return response(e)

    def put(self, request):
        try:
            form = StudentsForm(request.POST, request.FILES)

            student_id = request.POST('student_id')
            fio = request.POST('fio')
            participation_period = request.POST('participation_period')
            mounth = request.POST('mounth')
            level  = request.POST('level')
            category  = request.POST('category')
            document = request.FILES['document']
            teacher  = request.POST('teacher')
            result  = request.POST('result')
            participation_in_profile_shifts = request.POST('participation_in_profile_shifts')
            name_program = request.POST('name_program')


            Students.objects.filter(id=student_id).update(fio=fio, participation_period=participation_period, 
                                                            mounth=mounth, level=level, category=category, 
                                                            document=document, teacher=teacher,  result=result,
                                                            participation_in_profile_shifts=participation_in_profile_shifts,
                                                            name_program=name_program)

            return HttpResponse(status_code=200)
        
        except Exception as e:
            return response(e)

    def delete(self, request):
        try:
            student_id = request.POST('student_id')

            student = Students.objects.get(id=student_id)
            student.delete()

            return HttpResponse(status_code=200)
        
        except Exception as e:
            return response(e)

class Teacher(View):
    def get(self, request):
        try:
            fio = request.GET('fio') or None
            page = request.GET('page')
            per_page = 10 # лимит отображения на странице
            

            data = Teachers.objects.filter(fio=fio).values()

            total = data.count()


            if total%per_page != 0:
                total_page = total//per_page+1
            else:
                total_page = total / per_page
            
            teachers = {
                'data':data,
                'total': total,
                'per_page': per_page,
                'page': page,
                'total_page': total_page,
            }

            return JsonResponse(data=teachers, safe=False)
        
        except Exception as e:
            return response(e)
    
    def post(self, request):
        try:
            form = TeachersForm(request.POST, request.FILES)

            fio = request.POST('fio')
            participation_period = request.POST('participation_period')
            mounth = request.POST('mounth')
            level  = request.POST('level')
            category  = request.POST('category')
            document = request.FILES['document']
            result  = request.POST('result')
            kpk  = request.POST('kpk')
            publications  = request.POST('publications')

            
            Teacher.objects.create(fio, participation_period, mounth, level, category, document, result, kpk, 
                                                publications)


            return HttpResponse(status_code=200)

        except Exception as e:
            return response(e)

    def put(self, request):
        try:
            form = TeachersForm(request.POST, request.FILES)

            teacher_id = request.POST('student_id')
            fio = request.POST('fio')
            participation_period = request.POST('participation_period')
            mounth = request.POST('mounth')
            level  = request.POST('level')
            category  = request.POST('category')
            document = request.FILES['document']
            result  = request.POST('result')
            kpk  = request.POST('kpk')
            publications  = request.POST('publications')


            Teacher.objects.filter(id=teacher_id).update(fio=fio, participation_period=participation_period, 
                                                            mounth=mounth, level=level, category=category, 
                                                            document=document, result=result, kpk=kpk, publications=publications)

            return HttpResponse(status_code=200)
        
        except Exception as e:
            return response(e)

    def delete(self, request):
        try:
            teacher_id = request.POST('teacher_id')

            teacher = Teacher.objects.get(id=teacher_id)
            teacher.delete()

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


class ExportToExcel(View):
    def exportToExcelStudents(request):
        # на вход фильтры по категории, временнной период, результативность
        category = request.GET('category') or None
        mounth = request.GET('mounth') or None
        participation_period = request.GET('participation_period') or None
        result = request.GET('result') or None
        
        
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="students.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Информация об учениках')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['ФИО', 'Период участия', 'Месяц', 'Уровень', 'Категория', 'Учитель', 
                    'Результат', 'Участие в профильных сменах', 'Название программы']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        # rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')

        rows = Students.objects.filter(category=category, mounth=mounth, participation_period=participation_period,
                                        result=result).values_list('fio', 'participation_period', 'mounth',
                                        'level',  'category',  'teacher',  'result',  'participation_in_profile_shifts' ,
                                        'name_program').order_by(Lower('fio'))
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        

        wb.save(response)
        return response

    def exportToExcelTeachers(request):
        # на вход фильтры по категории, временнной период, результативность
        category = request.GET('category') or None
        mounth = request.GET('mounth') or None
        result = request.GET('result') or None
        kpk = request.GET('kpk') or None
        publications = request.GET('publications') or None
        
        
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="teachers.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Информация об учителях')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['ФИО', 'Период участия', 'Месяц', 'Уровень', 'Категория',
                    'Результат', 'КПК', 'Публикации']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = Teachers.objects.filter(category=category, mounth=mounth, kpk=kpk, publications=publications,
                                        result=result).values_list('fio', 'participation_period', 'mounth',
                                        'level',  'category', 'result',  'kpk' , 'publications').order_by(Lower('fio'))
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        

        wb.save(response)
        return response
