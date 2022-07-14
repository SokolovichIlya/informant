from django.db import models
from django.contrib.auth.models import User
from .config import Mounth, Level, Result

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

# Данные об учениках
class Students(models.Model):
    fio = models.CharField("ФИО", max_length=150)
    participation_period = models.CharField("Период участия", max_length=250)
    mounth = models.CharField("Месяц", max_length=2, default='0', choices=Mounth())
    level  = models.CharField("Уровень", max_length=1, default='0', choices=Level())
    category  = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
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
