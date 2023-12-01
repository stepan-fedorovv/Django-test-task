from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Direction, Discipline, Group, Student, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_curator', 'is_staff', )


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code', 'curator')


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'direction')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'group', 'sex')
