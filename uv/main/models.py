from django.db import models


# Create your models here.
class Teacher(models.Model):
    num_teacher = models.CharField(max_length=200, verbose_name='Номер преподавателя')
    first_name = models.CharField(max_length=200, verbose_name='Фамилия')
    second_name = models.CharField(max_length=200, verbose_name='Имя')
    email = models.EmailField(max_length=254, verbose_name='Почта')

    class Meta:
        verbose_name = 'преподавателя'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return self.num_teacher


class Courses(models.Model):
    num_course = models.CharField(max_length=200, verbose_name='Номер курса', unique=True)
    name_course = models.CharField(max_length=200, verbose_name='Название курса', unique=True)
    sheet_curse = models.CharField(max_length=200, verbose_name='Страница курса', unique=True)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.num_course


class Mailing(models.Model):
    num_course = models.ForeignKey(to=Courses, on_delete=models.CASCADE, verbose_name='Номер курса')
    num_teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE, verbose_name='Номер преподавателя')

    class Meta:
        verbose_name = 'рассылку'
        verbose_name_plural = 'Рассылка'


class SaveFile(models.Model):
    host_name = models.CharField(max_length=50, verbose_name='Сервер')
    file_name = models.CharField(max_length=200, verbose_name='Имя файла')
    file_path = models.CharField(max_length=200, verbose_name='Путь')
    user_name_samba = models.CharField(max_length=200, verbose_name='Имя пользователя')
    user_password_samba = models.CharField(max_length=200, verbose_name='Пароль')
    public_folder = models.CharField(max_length=200, null=True, verbose_name='Публичная папка')
    path_for_smb_linux = models.CharField(max_length=200, null=True, verbose_name='Путь для SMB Linux')

    def __str__(self):
        return self.file_name
