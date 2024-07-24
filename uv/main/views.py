import pandas as pd
import os
import smbclient
import traceback

from django.shortcuts import render
from main.models import SaveFile



def index(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'main/index.html', context)



def student_list(request):
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
            print(f'Ошибка')
            print(error)
        except FileExistsError as e:
            print(e)

    df = pd.read_excel('Список учеников 2024.xlsm', sheet_name='RX-СИ')
    df = df.dropna(subset='Компания').astype(str)
    df = df.fillna(0)
    df = df.rename(columns={'Фамилия': 'first_name', 'Имя': 'second_name', 'Отчество': 'last_name',
                            'Компания': 'company', 'Дата начала': 'date_start', 'Должность': 'position',
                            'Подразд.': 'unit'})
    df.loc[:, 'date_start'] = pd.to_datetime(df['date_start'], format='%Y-%m-%d').dt.strftime('%d-%m-%Y')
    df = df.fillna("0")
    students = df.to_dict('records')
    return render(request, 'main/student_list.html', {'students': students})
