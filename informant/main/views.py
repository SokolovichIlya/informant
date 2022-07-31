import imp
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
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

class HomePageView(TemplateView):
    template_name = "pages/home.html"

class TeacherPageView(TemplateView):
    template_name = "pages/teachers/list.html"

class StudentPageView(TemplateView):
    template_name = "pages/students/list.html"

class StudentAddPageView(TemplateView):
    template_name = "pages/students/add.html"

    def get_context_data(self, **kwargs):
        teachers = User.objects.all()
        categories = Categories.objects.all()
        subCategories = SubCategories.objects.all()
        profileShifts = ProfileShifts.objects.all()

        context = {
            'teachers': teachers,
            'categories': categories,
            'subCategories': subCategories,
            'profileShifts': profileShifts,
        }

        return context

class TeacherAddPageView(TemplateView):
    template_name = "pages/teachers/add.html"

    def get_context_data(self, **kwargs):
        categories = Categories.objects.all()
        subCategories = SubCategories.objects.all()
        kpk = Kpk.objects.filter(default_view = True)
        publications = Publications.objects.all()

        context = {
            'kpk': kpk,
            'categories': categories,
            'subCategories': subCategories,
            'publications': publications,
        }

        return context


class Student(View):
    def get(self, request):
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
 
    def post(self, request):
        try:
            if request.user.is_authenticated:
                id_category = SubCategories.objects.filter(name=request.POST.get('category')).values_list('category').first()[0]
                id_sub_category = SubCategories.objects.filter(name=request.POST.get('category')).values_list('pk').first()[0]

                fio = request.POST.get('fio')
                participation_period = request.POST.get('participation_period')
                mounth = request.POST.get('mounth')
                level  = request.POST.get('level')
                category  = Categories.objects.get(pk=id_category)
                sub_category  = SubCategories.objects.get(pk=id_sub_category)
                document = request.FILES['document']
                teacher  = User.objects.get(pk=request.POST.get('teacher'))
                result  = request.POST.get('result')
                participation_in_profile_shifts = ProfileShifts.objects.get(pk=request.POST.get('participation_in_profile_shifts'))
                name_program = request.POST.get('name_program')

                Students.objects.create(fio=fio, participation_period=participation_period, mounth=mounth, level=level, 
                                        category=category,sub_category=sub_category, document=document, teacher=teacher, 
                                        result=result, participation_in_profile_shifts=participation_in_profile_shifts, 
                                        name_program=name_program)


                return redirect('/students/')

        except Exception as e:
            print(e)
            return HttpResponse(status=401)

    def put(self, request):
        try:
            if request.user.is_authenticated:
                id_category = SubCategories.objects.filter(name=request.POST.get('category')).values_list('category').first()[0]
                id_sub_category = SubCategories.objects.filter(name=request.POST.get('category')).values_list('pk').first()[0]

                student_id = request.POST.get('student_id')

                fio = request.POST.get('fio')
                participation_period = request.POST.get('participation_period')
                mounth = request.POST.get('mounth')
                level  = request.POST.get('level')
                category  = Categories.objects.get(pk=id_category)
                sub_category  = SubCategories.objects.get(pk=id_sub_category)
                document = request.FILES['document']
                teacher  = User.objects.get(pk=request.POST.get('teacher'))
                result  = request.POST.get('result')
                participation_in_profile_shifts = ProfileShifts.objects.get(pk=request.POST.get('participation_in_profile_shifts'))
                name_program = request.POST.get('name_program')


            Students.objects.filter(id=student_id).update(fio=fio, participation_period=participation_period, 
                                                            mounth=mounth, level=level, category=category, 
                                                            sub_category=sub_category,
                                                            document=document, teacher=teacher,  result=result,
                                                            participation_in_profile_shifts=participation_in_profile_shifts,
                                                            name_program=name_program)

            return redirect('/students/')
        
        except Exception as e:
            return HttpResponse(status=401)

    def delete(self, request):
        try:
            student_id = request.POST.get('student_id')

            student = Students.objects.get(id=student_id)
            student.delete()

            return HttpResponse(status_code=200)
        
        except Exception as e:
            return HttpResponse(status=401)


class StudentDetail(View):
    def get(self, request, id):
        student = Students.objects.get(id = id)
        teachers = User.objects.all()
        categories = Categories.objects.all()
        subCategories = SubCategories.objects.all()
        profileShifts = ProfileShifts.objects.all()

        context = {
            'teachers': teachers,
            'categories': categories,
            'subCategories': subCategories,
            'profileShifts': profileShifts,
            'student': student,
        }


        return render(request, 'pages/students/detail.html', context) 


class Teacher(View):
    def get(self, request):
        try:
            fio = request.GET.get('fio') or None
            page = request.GET.get('page')
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
            return HttpResponse(status=401)
    
    def post(self, request):
        try:
            if request.user.is_authenticated:
                id_category = SubCategories.objects.filter(name=request.POST.get('category')).values_list('category').first()[0]
                id_sub_category = SubCategories.objects.filter(name=request.POST.get('category')).values_list('pk').first()[0]
                
                kpk_id  = request.POST.get('kpk')
                publications_name = request.POST.get('publications_name')
                publications_name_journal = request.POST.get('publications_name_journal')
                publications_city = request.POST.get('publications_city')
                publications_page_range = request.POST.get('publications_page_range')
                
                publications_id = Publications.objects.create(name=publications_name, 
                                    name_journal=publications_name_journal, 
                                    city=publications_city, 
                                    page_range=publications_page_range)


                fio = request.POST.get('fio')
                participation_period = request.POST.get('participation_period')
                mounth = request.POST.get('mounth')
                level  = request.POST.get('level')
                category  = Categories.objects.get(pk=id_category)
                sub_category  = SubCategories.objects.get(pk=id_sub_category)
                category_document = request.FILES['category_document']
                result  = request.POST.get('result')
                kpk = Kpk.objects.get(pk=kpk_id)
                kpk_document = request.FILES['kpk_document']
                publications  = Publications.objects.get(pk=publications_id.pk)
                publications_document = request.FILES['publications_document']
                

                Teachers.objects.create(fio=fio, participation_period=participation_period, mounth=mounth, 
                                        level=level, category=category,sub_category=sub_category, category_document=category_document, result=result, 
                                        kpk=kpk, kpk_document=kpk_document, publications=publications, 
                                        publications_document=publications_document)


                return redirect('/teachers/')

        except Exception as e:
            return HttpResponse(status=401)

    def put(self, request):
        try:
            if request.user.is_authenticated:
                teacher_id = request.POST.get('student_id')

                id_category = SubCategories.objects.filter(name=request.POST.get('category')).values_list('category').first()[0]
                id_sub_category = SubCategories.objects.filter(name=request.POST.get('category')).values_list('pk').first()[0]
                
                kpk_id  = request.POST.get('kpk')
                if kpk_id == None:
                    kpk_name = request.POST.get('kpk_name')
                    kpk_city = request.POST.get('kpk_city')
                    kpk_organization = request.POST.get('kpk_organization')
                    kpk_date_issue = request.POST.get('kpk_date_issue')
                    kpk_number_hours = request.POST.get('kpk_number_hours')

                    kpk_id = Kpk.objects.create(kpk_name=kpk_name, kpk_city=kpk_city, kpk_organization=kpk_organization, 
                                        kpk_date_issue=kpk_date_issue, kpk_number_hours=kpk_number_hours)
                    kpk_id = kpk_id.pk

                publications_name = request.POST.get('publications_name')
                publications_name_journal = request.POST.get('publications_name_journal')
                publications_city = request.POST.get('publications_city')
                publications_page_range = request.POST.get('publications_page_range')
                
                publications_id = Publications.objects.create(name=publications_name, 
                                    name_journal=publications_name_journal, 
                                    city=publications_city, 
                                    page_range=publications_page_range)


                fio = request.POST.get('fio')
                participation_period = request.POST.get('participation_period')
                mounth = request.POST.get('mounth')
                level  = request.POST.get('level')
                category  = Categories.objects.get(pk=id_category)
                sub_category  = SubCategories.objects.get(pk=id_sub_category)
                category_document = request.FILES['category_document']
                result  = request.POST.get('result')
                kpk = Kpk.objects.get(pk=kpk_id)
                kpk_document = request.FILES['kpk_document']
                publications  = Publications.objects.get(pk=publications_id.pk)
                publications_document = request.FILES['publications_document']
                

                Teachers.objects.filter(id=teacher_id).update(fio=fio, participation_period=participation_period, mounth=mounth, 
                                        level=level, category=category,sub_category=sub_category, category_document=category_document, result=result, 
                                        kpk=kpk, kpk_document=kpk_document, publications=publications, 
                                        publications_document=publications_document)


                return redirect('/teachers/')
        
        except Exception as e:
            return HttpResponse(status=401)

    def delete(self, request):
        try:
            teacher_id = request.POST.get('teacher_id')

            teacher = Teachers.objects.get(id=teacher_id)
            teacher.delete()

            return HttpResponse(status_code=200)
        
        except Exception as e:
            return HttpResponse(status=401)

class Kpk(View):
    def post(self, request):
        kpk_name = request.POST.get('kpk_name')
        kpk_city = request.POST.get('kpk_city')
        kpk_organization = request.POST.get('kpk_organization')
        kpk_date_issue = request.POST.get('kpk_date_issue')
        kpk_number_hours = request.POST.get('kpk_number_hours')

        kpk = Kpk.objects.create(kpk_name=kpk_name, kpk_city=kpk_city, kpk_organization=kpk_organization, 
                            kpk_date_issue=kpk_date_issue, kpk_number_hours=kpk_number_hours)

        test=dict(list(kpk))
        return JsonResponse(data=test, safe=False)



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    print(user)
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
        # на вход фильтры по категории, временнной период, результативность

        filters = {}

        category = request.GET.get('category') 
        if category != None:
            filters['category'] = category
        mounth = request.GET.get('mounth') 
        if mounth != None: 
            mounth = int(mounth)
            filters['mounth'] = mounth
        participation_period = request.GET.get('participation_period') 
        if participation_period != None:
            filters['participation_period'] = participation_period
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

        columns = ['ФИО', 'Период участия', 'Месяц', 'Уровень', 'Категория', 'Учитель', 
                    'Результат', 'Участие в профильных сменах', 'Название программы']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()


        if len(filters) != 0:
            rows = Students.objects.filter(**filters).values_list('fio', 'participation_period', 'mounth',
                                        'level',  'category',  'teacher',  'result',  'participation_in_profile_shifts' ,
                                        'name_program').order_by(Lower('fio'))
        else:
            rows = Students.objects.all().values_list('fio', 'participation_period', 'mounth',
                                        'level',  'category',  'teacher',  'result',  'participation_in_profile_shifts' ,
                                        'name_program').order_by(Lower('fio'))


        


        for row in rows:
            row = list(row)

            for mounth in Mounth():
                if mounth[0] == row[2]:
                    row[2] = mounth[1]

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

    def exportToExcelTeachers(request):
        # на вход фильтры по категории, временнной период, результативность
        filters = {}

        category = request.GET.get('category') 
        if category != None:
            filters['category'] = category
        mounth = request.GET.get('mounth') 
        if mounth != None: 
            mounth = int(mounth)
            filters['mounth'] = mounth
        result = request.GET.get('result') 
        if result != None: 
            result = int(result)
            filters['result'] = result
        kpk = request.GET.get('kpk') 
        if kpk != None:
            filters['kpk'] = kpk
        publications = request.GET.get('publications') 
        if publications != None:
            filters['publications'] = publications

        
        
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

        if len(filters) != 0:
            rows = Teachers.objects.filter(**filters).values_list('fio', 'participation_period', 'mounth',
                                        'level',  'category', 'result',  'kpk' , 'publications').order_by(Lower('fio'))
        else:
            rows = Teachers.objects.all().values_list('fio', 'participation_period', 'mounth',
                                        'level',  'category', 'result',  'kpk' , 'publications').order_by(Lower('fio'))

        for row in rows:
            row = list(row)

            for mounth in Mounth():
                if mounth[0] == row[2]:
                    row[2] = mounth[1]

            for level in Level():
                if level[0] == row[3]:
                    row[3] = level[1]

            row[4] = Categories.objects.get(pk=row[4]).name
            row[5] = Kpk.objects.get(pk=row[4]).name
            row[6]= Publications.objects.get(pk=row[7]).name

            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        

        wb.save(response)
        return response


class DownloadFile(View):
    def downloadFileStudents(request):
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
  
    def downloadFileTeachers(request):
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