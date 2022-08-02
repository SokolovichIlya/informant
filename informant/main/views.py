import imp
import re
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView, View
from django.contrib.auth.models import User
from django.db.models import *
from django.db.models.functions import Lower
from .models import *
from .config import *
from .forms import LoginForm, StudentsForm, TeachersForm
from django.conf import settings

import operator
import datetime
import json
import os
import xlwt

def customDateSerialize(o):
    if isinstance(o, datetime.date):
        return o.__str__()

class HomePageView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = None
    template_name = "pages/home.html"

class TeacherPageView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = None
    template_name = "pages/teachers/list.html"

class StudentPageView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = None
    template_name = "pages/students/list.html"

class StudentAddPageView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = None
    template_name = "pages/students/add.html"

    def get_context_data(self, **kwargs):
        teachers = User.objects.all().values()
        categories = Categories.objects.all().values()
        subCategories = SubCategories.objects.all().values()
        profileShifts = ProfileShifts.objects.all().values()

        context = {
            'categories': json.dumps(list(categories), default=customDateSerialize),
            'subCategories': json.dumps(list(subCategories), default=customDateSerialize),
            'teachers': json.dumps(list(teachers), default=customDateSerialize),
            'profileShifts': json.dumps(list(profileShifts)),
        }

        return context

class TeacherAddPageView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = None
    template_name = "pages/teachers/add.html"

    def get_context_data(self, **kwargs):
        categories = Categories.objects.all().values()
        subCategories = SubCategories.objects.all().values()
        kpk = Kpk.objects.filter(default_view = True).values()
        publications = Publications.objects.all().values()

        context = {
            'categories': json.dumps(list(categories), default=customDateSerialize),
            'subCategories': json.dumps(list(subCategories), default=customDateSerialize),
            'kpk': json.dumps(list(kpk), default=customDateSerialize),
            'publications': json.dumps(list(publications), default=customDateSerialize),
        }

        return context

class ReportsPageView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = None
    template_name = "pages/reports/index.html"

    def get_context_data(self, **kwargs):
        teachers = User.objects.all().values()
        kpk = Kpk.objects.filter().values()

        context = {
            'teachers': json.dumps(list(teachers), default=customDateSerialize),
            'kpk': json.dumps(list(kpk), default=customDateSerialize),
        }

        return context


class Student(View):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                fio = request.GET.get('fio') or None
                page = request.GET.get('page')
                per_page = 10 # лимит отображения на странице
                
                if fio:
                    data = Students.objects.filter(fio=fio).values()
                else:
                    data = Students.objects.all().values()

                total = data.count()

                if total%per_page != 0:
                    total_page = total//per_page+1
                else:
                    total_page = total / per_page
                
                students = {
                    'data': list(data),
                    'total': total,
                    'per_page': per_page,
                    'page': page,
                    'total_page': total_page,
                }

                return JsonResponse(data=students, safe=False)
            
            except Exception as e:
                return HttpResponse(status=401)
        else:
            return redirect('/login')

    def post(self, request):
        if request.user.is_authenticated:
            try:
                fio = request.POST.get('fio')
                date_from = request.POST.get('date_from') 
                date_to = request.POST.get('date_to') 
                level  = request.POST.get('level')
                category  = Categories.objects.get(pk=request.POST.get('category'))
                sub_category  = SubCategories.objects.get(pk=request.POST.get('sub_category'))
                document = request.FILES['document']
                teacher  = User.objects.get(pk=request.POST.get('teacher'))
                result  = request.POST.get('result')
                participation_in_profile_shifts = ProfileShifts.objects.get(pk=request.POST.get('participation_in_profile_shifts'))
                name_program = request.POST.get('name_program')

                Students.objects.create(fio=fio, date_from=date_from, date_to=date_to, level=level, 
                                        category=category,sub_category=sub_category, document=document, teacher=teacher, 
                                        result=result, participation_in_profile_shifts=participation_in_profile_shifts, 
                                        name_program=name_program)


                return redirect('/students/')

            except Exception as e:
                print(e)
                return HttpResponse(status=500)
        else:
            return redirect('/login')

    def update(request):
        if request.user.is_authenticated:
            try:
                student_id = request.POST.get('id')
                fio = request.POST.get('fio')
                date_from = request.POST.get('date_from') 
                date_to = request.POST.get('date_to')
                level  = request.POST.get('level')
                category  = Categories.objects.get(id=request.POST.get('category'))
                sub_category  = SubCategories.objects.get(id=request.POST.get('sub_category'))
                teacher  = User.objects.get(pk=request.POST.get('teacher'))
                result  = request.POST.get('result')
                participation_in_profile_shifts = ProfileShifts.objects.get(id=request.POST.get('participation_in_profile_shifts'))
                name_program = request.POST.get('name_program')


                Students.objects.filter(id=student_id).update(fio=fio, date_from=date_from, date_to=date_to,
                                                                level=level, category=category, 
                                                                sub_category=sub_category, teacher=teacher,  result=result,
                                                                participation_in_profile_shifts=participation_in_profile_shifts,
                                                                name_program=name_program)

                return redirect('/students/')
            
            except Exception as e:
                print(e)
                return HttpResponse(status=500)
        else:
            return redirect('/login')

    def delete(request):
        if request.user.is_authenticated:
            try:
                student_id = request.POST.get('id')

                student = Students.objects.get(id=student_id)

                student.delete()

                return HttpResponse(status=200)
            
            except Exception as e:
                print(e)
                return HttpResponse(status=500)
        else:
            return redirect('/login')

class StudentDetail(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            student = Students.objects.filter(id = id).values()
            teachers = User.objects.all().values()
            categories = Categories.objects.all().values()
            subCategories = SubCategories.objects.all().values()
            profileShifts = ProfileShifts.objects.all().values()

            context = {
                'teachers': json.dumps(list(teachers), default=customDateSerialize),
                'categories': json.dumps(list(categories), default=customDateSerialize),
                'subCategories': json.dumps(list(subCategories), default=customDateSerialize),
                'profileShifts': json.dumps(list(profileShifts), default=customDateSerialize),
                'student': json.dumps(list(student), default=customDateSerialize),
            }


            return render(request, 'pages/students/detail.html', context) 
        else:
            return redirect('/login')

class Teacher(View):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                fio = request.GET.get('fio') or None
                page = request.GET.get('page')
                per_page = 10 # лимит отображения на странице
                
                if fio:
                    data = Teachers.objects.filter(fio=fio).values()
                else:
                    data = Teachers.objects.all().values()

                total = data.count()


                if total%per_page != 0:
                    total_page = total//per_page+1
                else:
                    total_page = total / per_page
                
                teachers = {
                    'data': list(data),
                    'total': total,
                    'per_page': per_page,
                    'page': page,
                    'total_page': total_page,
                }

                return JsonResponse(data=teachers, safe=False)
            
            except Exception as e:
                return HttpResponse(status=401)
        else:
            return redirect('/login')

    def post(self, request):
        if request.user.is_authenticated:
            try:
                publications_name = request.POST.get('publications_name')
                publications_name_journal = request.POST.get('publications_name_journal')
                publications_city = request.POST.get('publications_city')
                publications_page_range = request.POST.get('publications_page_range')
                
                publications_id = Publications.objects.create(name=publications_name, 
                                    name_journal=publications_name_journal, 
                                    city=publications_city, 
                                    page_range=publications_page_range)

                fio = request.POST.get('fio')
                date_from = request.POST.get('date_from') 
                date_to = request.POST.get('date_to')
                level  = request.POST.get('level')
                category  = Categories.objects.get(pk=request.POST.get('category'))
                sub_category  = SubCategories.objects.get(pk=request.POST.get('sub_category'))
                category_document = request.FILES['document']
                result  = request.POST.get('result')
                kpk = Kpk.objects.get(pk=request.POST.get('kpk'))
                kpk_document = request.FILES['documentKpk']
                publications  = Publications.objects.get(pk=publications_id.pk)
                publications_document = request.FILES['documentPublication']
                
                Teachers.objects.create(fio=fio, date_from=date_from, date_to=date_to,
                                        level=level, category=category,sub_category=sub_category, category_document=category_document, result=result, 
                                        kpk=kpk, kpk_document=kpk_document, publications=publications, 
                                        publications_document=publications_document)


                return redirect('/teachers/')

            except Exception as e:
                print(e)
                return HttpResponse(status=401)
        else:
            return redirect('/login')
    def update(request):
        if request.user.is_authenticated:
            try:
                teacher_id = request.POST.get('id')
    
                publications_name = request.POST.get('publications_name')
                publications_name_journal = request.POST.get('publications_name_journal')
                publications_city = request.POST.get('publications_city')
                publications_page_range = request.POST.get('publications_page_range')
                
                publications_id = Publications.objects.create(name=publications_name, 
                                    name_journal=publications_name_journal, 
                                    city=publications_city, 
                                    page_range=publications_page_range)

                fio = request.POST.get('fio')
                date_from = request.POST.get('date_from') 
                date_to = request.POST.get('date_to')
                level  = request.POST.get('level')
                category  = Categories.objects.get(id=request.POST.get('category'))
                sub_category  = SubCategories.objects.get(id=request.POST.get('sub_category'))
                result  = request.POST.get('result')
                kpk = Kpk.objects.get(pk=request.POST.get('kpk'))
                publications  = Publications.objects.get(pk=publications_id.pk)
                

                Teachers.objects.filter(id=teacher_id).update(fio=fio, date_from=date_from, date_to=date_to, 
                                        level=level, category=category,sub_category=sub_category, result=result, 
                                        kpk=kpk, publications=publications)

                return redirect('/teachers/')
            
            except Exception as e:
                return HttpResponse(status=401)
        else:
            return redirect('/login')
    def delete(request):
        if request.user.is_authenticated:
            try:
                teacher_id = request.POST.get('id')

                teacher = Teachers.objects.get(id=teacher_id)

                teacher.delete()

                return HttpResponse(status=200)
            
            except Exception as e:
                print(e)
                return HttpResponse(status=500)
        else:
            return redirect('/login')

class KpkView(View):
    def post(self, request):
        if request.user.is_authenticated:
            kpk_name = request.POST.get('kpk_name')
            kpk_city = request.POST.get('kpk_city')
            kpk_organization = request.POST.get('kpk_organization')
            kpk_date_issue = request.POST.get('kpk_date_issue')
            kpk_number_hours = request.POST.get('kpk_number_hours')

            kpk = Kpk.objects.create(name=kpk_name, city=kpk_city, organization=kpk_organization, 
                                date_issue=kpk_date_issue, number_hours=kpk_number_hours)

            returnKPK = Kpk.objects.filter(id = kpk.id).values()

            return JsonResponse(data=json.dumps(list(returnKPK), default=customDateSerialize), safe=False)
        else:
            return redirect('/login')

    def update(request):
        if request.user.is_authenticated:
            kpk_id = request.POST.get('id')
            kpk_name = request.POST.get('kpk_name') 
            kpk_city = request.POST.get('kpk_city') or None
            kpk_organization = request.POST.get('kpk_organization') or None
            kpk_date_issue = request.POST.get('kpk_date_issue') or None
            kpk_number_hours = request.POST.get('kpk_number_hours') or None

            Kpk.objects.filter(id=kpk_id).update(name=kpk_name, city=kpk_city, organization=kpk_organization, 
                                date_issue=kpk_date_issue, number_hours=kpk_number_hours)

            returnKPK = Kpk.objects.filter(id = kpk_id).values()

            return JsonResponse(data=json.dumps(list(returnKPK), default=customDateSerialize), safe=False)
        else:
            return redirect('/login')

class TeacherDetail(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            teacher = Teachers.objects.filter(id = id).values(
                'id',
                'fio',
                'date_from',
                'date_to',
                'level',
                'category',
                'sub_category',
                'category_document',
                'result',
                'kpk__id',
                'kpk__name',
                'kpk__city',
                'kpk__organization',
                'kpk__date_issue',
                'kpk__number_hours',
                'kpk_document',
                'publications__id',
                'publications__name',
                'publications__name_journal',
                'publications__city',
                'publications__page_range',
                'publications_document',
            )

            categories = Categories.objects.all().values()
            subCategories = SubCategories.objects.all().values()
            kpk = Kpk.objects.filter(default_view = True).values()
            publications = Publications.objects.all().values()

            context = {
                'teacher': json.dumps(list(teacher), default=customDateSerialize),
                'categories': json.dumps(list(categories), default=customDateSerialize),
                'subCategories': json.dumps(list(subCategories), default=customDateSerialize),
                'kpk': json.dumps(list(kpk), default=customDateSerialize),
                'publications': json.dumps(list(publications), default=customDateSerialize),
            }

            return render(request, 'pages/teachers/detail.html', context) 
        else:
            return redirect('/login')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse(status_code=401)
            else:
                return HttpResponse(status_code=403)
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def logout(request):
    django_logout(request)
    return redirect('/login')


class ExportToExcel(View):
    def exportToExcelStudents(request):
        # на вход фильтры по период времени,   категории, результативность
        if request.user.is_authenticated:
            filters = {}

            date_from = request.GET.get('date_from') 
            date_to = request.GET.get('date_to') 

            date_from = request.GET.get('date_from') 
            if date_from != None:
                filters['date_from__gte'] = date_from
            
            date_to = request.GET.get('date_to') 
            if date_to != None:
                filters['date_to__lte'] = date_to


            category = request.GET.get('category') 
            if category != None:
                if category == 3:
                    filters['participation_in_profile_shifts__isnull'] = False
                else:
                    filters['category'] = category

            result = request.GET.get('result') 
            if result != None: 
                result = int(result)
                filters['result'] = result

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="students.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Информация об учениках')

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['ФИО', 'Дата с', 'Дата по', 'Уровень', 'Категория', 'Учитель', 
                        'Результат', 'Участие в профильных сменах', 'Название программы']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()


            rows = Students.objects.filter(**filters).values_list('fio', 'date_from', 'date_to',
                                            'level',  'category',  'teacher',  'result',  'participation_in_profile_shifts' ,
                                            'name_program').order_by(Lower('fio'))


            for row in rows:
                row = list(row)

                row[1] = row[1].strftime("%d.%m.%Y")
                row[2] = row[2].strftime("%d.%m.%Y")

                for level in Level():
                    if level[0] == row[3]:
                        row[3] = level[1]

                row[4] = Categories.objects.get(pk=row[4]).name
                row[5] = User.objects.get(pk=row[5]).username

                for result in Result():
                    if result[0] == row[6]:
                        row[6] = result[1]

                row[7]= ProfileShifts.objects.get(pk=row[7]).name

                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            

            wb.save(response)
            return response
        else:
            return redirect('/login')

    def exportToExcelTeachers(request):
        # на вход фильтры по категории, временнной период, результативность
        if request.user.is_authenticated:
            filters = {}
            filters_student = {}

            fio = request.GET.get('fio') 
            if fio != None:
                filters['fio'] = Teachers.objects.get(pk=request.GET.get('fio')).fio    
                filters_student['teacher'] = Teachers.objects.get(pk=request.GET.get('fio')).fio 


            date_from = request.GET.get('date_from') 
            if date_from != None:
                filters['date_from__gte'] = date_from
            
            date_to = request.GET.get('date_to') 
            if date_to != None:
                filters['date_to__lte'] = date_to

            category = request.GET.get('category') 
            kpk = request.GET.get('kpk') 

            if category != None:
                if category == 3:
                    if kpk != None:
                        filters['kpk'] = kpk
                    else:
                        filters['kpk__isnull'] = False
                elif category == 4:
                    filters['publications__isnull'] = False
                else:
                    filters['category'] = category


            result = request.GET.get('result') 
            if result != None: 
                result = int(result)
                filters['result'] = result

            student_category = request.GET.get('student_category') 
            if student_category != None: 
                filters_student['category'] = student_category

            student_result = request.GET.get('student_result') 
            if student_result != None: 
                student_result = int(student_result)
                filters_student['result'] = student_result

            
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="teachers.xls"'

            wb = xlwt.Workbook(encoding='utf-8')

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            if student_category or student_result:
                ws = wb.add_sheet(fio)

                columns = ['ФИО', 'Дата с', 'Дата по', 'Уровень', 'Категория', 'Учитель', 
                        'Результат', 'Участие в профильных сменах', 'Название программы']

                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)

                # Sheet body, remaining rows
                font_style = xlwt.XFStyle()

                rows = Students.objects.filter(**filters).values_list('fio', 'date_from', 'date_to',
                                                'level',  'category',  'teacher',  'result',  'participation_in_profile_shifts' ,
                                                'name_program').order_by(Lower('fio'))
                for row in rows:
                    row = list(row)

                    row[1] = row[1].strftime("%d.%m.%Y")
                    row[2] = row[2].strftime("%d.%m.%Y")

                    for level in Level():
                        if level[0] == row[3]:
                            row[3] = level[1]

                    row[4] = Categories.objects.get(pk=row[4]).name
                    row[5] = User.objects.get(pk=row[5]).username

                    for result in Result():
                        if result[0] == row[6]:
                            row[6] = result[1]

                    row[7]= ProfileShifts.objects.get(pk=row[7]).name

                    row_num += 1
                    for col_num in range(len(row)):
                        ws.write(row_num, col_num, row[col_num], font_style)
                
            else:
                ws = wb.add_sheet(f'Информация об учителях')

                columns = ['ФИО', 'Дата с', 'Дата по', 'Уровень', 'Категория',
                            'Результат', 'КПК', 'Публикации']

                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)

                # Sheet body, remaining rows
                font_style = xlwt.XFStyle()

                rows = Teachers.objects.filter(**filters).values_list('fio', 'date_from', 'date_to',
                                                'level',  'category', 'result',  'kpk' , 'publications').order_by(Lower('fio'))

                for row in rows:
                    row = list(row)

                    row[1] = row[1].strftime("%d.%m.%Y")
                    row[2] = row[2].strftime("%d.%m.%Y")

                    for level in Level():
                        if level[0] == row[3]:
                            row[3] = level[1]

                    row[4] = Categories.objects.get(pk=row[4]).name
                    row[6] = Kpk.objects.get(pk=row[6]).name
                    row[7]= Publications.objects.get(pk=row[7]).name

                    row_num += 1
                    for col_num in range(len(row)):
                        ws.write(row_num, col_num, row[col_num], font_style)
                
            wb.save(response)
            return response
        else:
            return redirect('/login')

class DownloadFile(View):
    def downloadFileStudents(request):
        if request.user.is_authenticated:
            student_id = request.GET.get('student_id')

            fileStudent = Students.objects.values_list('document').get(id=student_id)

            file_name = fileStudent[0].split('/')


            path_download = f"{settings.MEDIA_ROOT}\\{fileStudent[0]}"

            if os.path.exists(path_download):
                with open(path_download, 'rb') as fl:
                    response = HttpResponse(fl.read(), charset='utf-8')
                    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name[1])
                    response['Content-Length'] = os.path.getsize(path_download)
                    return response
        else:
            return redirect('/login')
            
    def downloadFileTeachers(request):
        if request.user.is_authenticated:
            teacher_id = request.GET.get('teacher_id')

            fileTeacher = Teachers.objects.values_list('document').get(id=teacher_id)
            file_name = fileTeacher[0].split('/')


            path_download = f"{settings.MEDIA_ROOT}\\{fileTeacher[0]}"

            if os.path.exists(path_download):
                with open(path_download, 'rb') as fl:
                    response = HttpResponse(fl.read(), charset='utf-8')
                    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name[1])
                    response['Content-Length'] = os.path.getsize(path_download)
                    return response
        else:
            return redirect('/login')    