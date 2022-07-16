from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.db.models import *

import datetime
import json

def customDateSerialize(o):
    if isinstance(o, datetime.date):
        return o.__str__()

class HomePageView(TemplateView):

    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        # teachers = Teachers.objects.all()
        # groups = GroupsSchool.objects.all()

        context = {'teachers': None, 'groups': None}

        return context

class TeacherPageView(TemplateView):

    template_name = "pages/teachers/list.html"

    def get_context_data(self, **kwargs):
        # teachers = Teachers.objects.all()
        # groups = GroupsSchool.objects.all()

        teachers = {
            'data': [
                {
                    'fio': 'Иванов Иван Иванович',
                    'fio_1': 'Иванов Иван Иванович1',
                    'fio_2': 'Иванов Иван Иванович2',
                    'fio_3': 'Иванов Иван Иванович3',
                },
                {
                    'fio': 'Иванов Иван Иванович',
                    'fio_1': 'Иванов Иван Иванович1',
                    'fio_2': 'Иванов Иван Иванович2',
                    'fio_3': 'Иванов Иван Иванович3',
                },
                {
                    'fio': 'Иванов Иван Иванович',
                    'fio_1': 'Иванов Иван Иванович1',
                    'fio_2': 'Иванов Иван Иванович2',
                    'fio_3': 'Иванов Иван Иванович3',
                },
            ],
            'total': 3,
            'per_page': 10,
            'page': 1,
            'total_page': 1,
        }

        context = {'teachers': json.dumps(teachers), 'groups': None}

        return context

class StudentPageView(TemplateView):

    template_name = "pages/students/list.html"

    def get_context_data(self, **kwargs):
        # teachers = Teachers.objects.all()
        # groups = GroupsSchool.objects.all()

        context = {'teachers': None, 'groups': None}

        return context