# Generated by Django 5.0.4 on 2024-06-03 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_emailsender_name_sheet_curse'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaveFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(max_length=50)),
                ('file_name', models.CharField(max_length=200)),
                ('file_path', models.CharField(max_length=200)),
                ('user_name_samba', models.CharField(max_length=200)),
                ('user_password_samba', models.CharField(max_length=200)),
            ],
        ),
    ]
