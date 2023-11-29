from django.db import models


class Curator(models.Model):
    name = models.CharField(max_length=255, verbose_name="Curator name")
    surname = models.CharField(max_length=255, verbose_name="Curator surname")
    bio = models.TextField(null=True, blank=True, verbose_name="Curator bio")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Curator"
        verbose_name_plural = "Curators"


class Direction(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title of direction")
    code = models.CharField(max_length=8, verbose_name="Code of direction")
    curator = models.ForeignKey(to=Curator, on_delete=models.DO_NOTHING, verbose_name="Curator of direction")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Direction"
        verbose_name_plural = "Directions"


class Discipline(models.Model):
    title = models.CharField(max_length=255, verbose_name="Discipline name")
    direction = models.ForeignKey(to=Direction, on_delete=models.CASCADE, verbose_name="Direction of discipline")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Discipline"
        verbose_name_plural = "Disciplines"


class Group(models.Model):
    title = models.CharField(max_length=255, verbose_name="Group title")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"


class Student(models.Model):
    name = models.CharField(max_length=255, verbose_name="Student name")
    surname = models.CharField(max_length=255, verbose_name="Student surname")
    picture = models.ImageField(verbose_name="Student profile picture")
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, verbose_name="Student Group")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
