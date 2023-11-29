from django.contrib import admin
from .models import Curator, Direction, Discipline, Group, Student


@admin.register(Curator)
class CuratorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'bio',)


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
    list_display = ('id', 'name', 'surname', 'picture', 'group',)
