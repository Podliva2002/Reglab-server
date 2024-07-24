from django.contrib import admin
from main.models import Teacher, SaveFile, Courses, Mailing

# Register your models here.

admin.site.register(SaveFile)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('num_teacher', 'first_name', 'second_name', 'email')
    search_fields = ('first_name',)
    ordering = ('num_teacher',)


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('num_course', 'name_course', 'sheet_curse')

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('num_course', 'num_teacher')
