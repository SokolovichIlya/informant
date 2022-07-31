from django.db import models
from django.contrib.auth.models import User
from .config import Mounth, Level, Result, TypeKpk

# Категории
class Categories(models.Model):
    name = models.CharField("Наименование", max_length=1000)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

# Подкатегории
class SubCategories(models.Model):
    name = models.CharField("Наименование", max_length=1000)
    category  = models.ForeignKey(Categories, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

# Профильные смены
class ProfileShifts(models.Model):
    name = models.CharField("Наименование", max_length=1000)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Профильная смена'
        verbose_name_plural = 'Профильные смены'

# КПК
class Kpk(models.Model):
    name = models.CharField("Название курсов в соответствии с удостоверением", max_length=1000)
    city = models.CharField("Город", max_length=1000, blank=True, null = True)
    organization = models.CharField("Организация в соответствии с удостоверением", max_length=1000,  blank=True, null = True)
    date_issue = models.DateField("Дата выдачи", max_length=1000,  blank=True, null = True)
    number_hours = models.IntegerField("Количество часов",  blank=True, null = True)
    default_view = models.BooleanField("Показывать по умолчанию", default=False) 

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'КПК'
        verbose_name_plural = 'КПК'

# Публикации
class Publications(models.Model):
    name = models.CharField("Название публиации", max_length=150)
    name_journal = models.CharField("Название журнала / сборника", max_length=1000)
    city = models.CharField("Город исздательства", max_length=1000)
    page_range = models.CharField("Диапазон страниц", max_length=1000)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Публикации'
        verbose_name_plural = 'Публикации'


# Данные об учениках
class Students(models.Model):
    fio = models.CharField("ФИО", max_length=150)
    date_from = models.DateField("Дата с", max_length=250)
    date_to = models.DateField("Дата по", max_length=250)
    level  = models.CharField("Уровень", max_length=1, default='0', choices=Level())
    category  = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category  = models.ForeignKey(SubCategories, on_delete=models.SET_NULL, null=True, blank=True) 
    document = models.FileField(upload_to='documents/')
    teacher  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    result  = models.CharField("Результат", max_length=1, default='2', choices=Result())
    participation_in_profile_shifts = models.ForeignKey(ProfileShifts, on_delete=models.SET_NULL, null=True, blank=True)
    name_program = models.CharField("Название программы", max_length=1000)

    class Meta:
        verbose_name = 'Данные об ученике'
        verbose_name_plural = 'Данные об учениках'

    def __str__(self):
        return self.fio


# Данные об учителях 
class Teachers(models.Model):
    fio = models.CharField("ФИО", max_length=150)
    date_from = models.DateField("Дата с", max_length=250)
    date_to = models.DateField("Дата по", max_length=250)
    level  = models.CharField("Уровень", max_length=1, default='0', choices=Level())
    category  = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category  = models.ForeignKey(SubCategories, on_delete=models.SET_NULL, null=True, blank=True) 
    category_document = models.FileField(upload_to='documents/')
    result  = models.CharField("Результат", max_length=1, default='2', choices=Result())
    kpk = models.ForeignKey(Kpk, on_delete=models.SET_NULL, null=True, blank=True)
    kpk_document = models.FileField(upload_to='documents/')
    publications  = models.ForeignKey(Publications, on_delete=models.SET_NULL, null=True, blank=True)
    publications_document = models.FileField(upload_to='documents/')


    class Meta:
        verbose_name = 'Данные об учителе'
        verbose_name_plural = 'Данные об учителе'

    def __str__(self):
        return self.fio
