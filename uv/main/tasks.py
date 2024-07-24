
from uv.celery import app
from django.core.mail import send_mail
from main.models import Teacher, Courses, Mailing, SaveFile
from datetime import datetime
from django.template import Template, Context

import pandas as pd
import os
import smbclient
import traceback


@app.task
def email():
    queryset = SaveFile.objects.first()
    hostname = queryset.host_name
    share_name = queryset.file_path
    username = queryset.user_name_samba
    password = queryset.user_password_samba
    remote_file_path = queryset.file_name
    local_file_path = "/home/ilya/Sender/uv/Список учеников 2024.xlsm"
    public_folder = queryset.public_folder
    path_samba = queryset.path_for_smb_linux

    # Копирование файла с удаленного сервера на локальный компьютер. Необходимо в чтени/записи ставить доп параметр b-binary
    # Samba server работает с файлами в двоичном формате

    def error_mail(file, txt_error):
        send_mail(
            f'Ошибка с получением файла {file}',
            f'{txt_error}',
            'Pod.liv.a@yandex.ru',
            ['i.agafonov@reglab.ru'],
            fail_silently=False,
        )

    try:
        with smbclient.open_file(f"//{hostname}/{share_name}/{remote_file_path}", username=username,
                                 password=password, mode="rb") as remote_file:
            with open(local_file_path, mode="wb") as local_file:
                local_file.write(remote_file.read())
    except:
        try:
            list_of_students_file = "Список учеников 2024.xlsm"
            os.system(
                f"smbclient \'\\\{hostname}\{public_folder}\\"
                f"' -U \'{username}%{password}\' -c \'cd \""
                f"{path_samba}\"; get \""
                + list_of_students_file + "\";  dir\'"
            )
            error = traceback.format_exc()
            error_mail(remote_file_path, error)

        except FileExistsError as e:
            error_mail(remote_file_path, e)

    df = pd.read_excel('Список учеников 2024.xlsm', sheet_name='График')
    #  Удаляем строки для корректеой работы
    # df = df.drop(df.index[15:25])
    df = df.fillna(-1)
    # Получаем текущий день в году 1-365
    num_day = int(datetime.today().strftime("%j"))

    # Проходимся по БД с преподавателями и курсами
    for mail in Mailing.objects.all():
        course = Courses.objects.get(num_course=mail.num_course)
        teacher = Teacher.objects.get(num_teacher=mail.num_teacher)
        condition = df['Unnamed: 1'] == str(course.name_course)
        row_number = df[condition].index[0]  # Получаем номер строки
        col_name_one_day = 'Unnamed: {}'.format(num_day + 4)
        col_name_seven_day = 'Unnamed: {}'.format(num_day + 10)

        name_teacher = df.loc[row_number, 'Unnamed: 2']

        num_of_persons = df.loc[row_number, col_name_one_day]
        num_of_persons_seven = df.loc[row_number, col_name_seven_day]
        df_person = pd.read_excel('Список учеников 2024.xlsm',
                                  sheet_name=str(course.sheet_curse))
        df_person = df_person.dropna(subset='Компания').astype(str)
        df_person = df_person.drop(columns=['Email', 'Дата окончания', 'Подразд.',
                                            "Сертификат", "Сгенерировать", "№"], axis=1)
        df_person = df_person.rename(columns={'Фамилия': 'first_name', 'Имя': 'second_name',
                                              'Отчество': 'last_name', 'Компания': 'company',
                                              'Дата начала': 'date_start', 'Должность': 'position'
                                              })
        df_person['date_start'] = pd.to_datetime(df_person['date_start'])
        # Конвертация даты начала в формат от 1 до 365
        df_person['date_start'] = df_person['date_start'].dt.dayofyear
        # Получение списка учеников на дату проводимого курса
        df_new = df_person[df_person['date_start'] == num_day + 1]
        df_new = df_new.drop(columns=['date_start'], axis=1)
        df_new.reset_index(drop=True, inplace=True)
        df_new.index += 1
        df_new = df_new['company']
        df_new = df_new.drop_duplicates()
        df_new = df_new.to_frame()
        df_new = df_new.rename(columns={'company': 'Компания'})

        df_new_seven = df_person[df_person['date_start'] == num_day + 7]
        df_new_seven = df_new_seven.drop(columns=['date_start'], axis=1)
        df_new_seven.reset_index(drop=True, inplace=True)
        df_new_seven.index += 1
        df_new_seven = df_new_seven['company']
        df_new_seven = df_new_seven.drop_duplicates()
        df_new_seven = df_new_seven.to_frame()
        df_new_seven = df_new_seven.rename(columns={'company': 'Компания'})

        # Проверка есть ли завтра на курсе ученики
        def mail(data, person, header, text):
            html = data.to_html()
            txt = str(int(person))
            name = name_teacher
            template = Template('На курс записано {{ person }} человек. Преподаватель/куратор {{teacher}}')
            context = Context({'person': txt, 'teacher': name})
            html_content = template.render(context)
            html += html_content
            send_mail(
                subject=header,
                message=text,
                from_email='Pod.liv.a@yandex.ru',
                recipient_list=[teacher.email],
                html_message=html,
                fail_silently=False,
            )

        if (num_of_persons is not None
                and num_of_persons not in [0, -1]):
            mail(df_new, num_of_persons, f'Завтра курс по {str(course.name_course)}', f'Заглушка')

        # Проверка есть ли за неделю на курсе ученики
        if (num_of_persons_seven > -1
                and not num_of_persons_seven == 0):
            mail(df_new_seven, num_of_persons_seven, f'Через 7 дней курс по {str(course.name_course)}', f'Заглушка')

        if (num_of_persons_seven == 0
                or num_of_persons == 0):
            send_mail(
                subject=f'На курс {str(course.name_course)} нет записи',
                message=f'На это уведомление не надо отвечать',
                from_email='Pod.liv.a@yandex.ru',
                recipient_list=[teacher.email],
                fail_silently=False,
            )