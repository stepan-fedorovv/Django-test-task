from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_curator = models.BooleanField(default=False)


class Direction(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title of direction")
    code = models.CharField(max_length=8, verbose_name="Code of direction")
    curator = models.ForeignKey(to=CustomUser,
                                on_delete=models.CASCADE,
                                verbose_name="Curator of direction",
                                limit_choices_to={"is_curator": True})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Direction"
        verbose_name_plural = "Directions"


class Discipline(models.Model):
    title = models.CharField(max_length=255, verbose_name="Discipline name")
    direction = models.ForeignKey(to=Direction,
                                  on_delete=models.CASCADE,
                                  verbose_name="Direction of discipline", )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Discipline"
        verbose_name_plural = "Disciplines"


class Group(models.Model):
    title = models.CharField(max_length=255, verbose_name="Group title")
    curator = models.ForeignKey(to=CustomUser,
                                on_delete=models.DO_NOTHING,
                                verbose_name="Curator of group",
                                limit_choices_to={"is_curator": True})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"


class Student(models.Model):
    CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    name = models.CharField(max_length=255, verbose_name="Student name")
    surname = models.CharField(max_length=255, verbose_name="Student surname")
    sex = models.CharField(max_length=255, choices=CHOICES)
    group = models.ForeignKey(to=Group,
                              on_delete=models.CASCADE,
                              verbose_name="Student Group", )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
