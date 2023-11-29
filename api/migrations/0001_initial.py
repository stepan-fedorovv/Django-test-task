# Generated by Django 4.2.7 on 2023-11-29 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Curator name')),
                ('surname', models.CharField(max_length=255, verbose_name='Curator surname')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Curator bio')),
            ],
            options={
                'verbose_name': 'Curator',
                'verbose_name_plural': 'Curators',
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title of direction')),
                ('code', models.CharField(max_length=8, verbose_name='Code of direction')),
                ('curator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.curator', verbose_name='Curator of direction')),
            ],
            options={
                'verbose_name': 'Direction',
                'verbose_name_plural': 'Directions',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Group title')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Student name')),
                ('surname', models.CharField(max_length=255, verbose_name='Student surname')),
                ('picture', models.ImageField(upload_to='', verbose_name='Student profile picture')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.group', verbose_name='Student Group')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Discipline name')),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.direction', verbose_name='Direction of discipline')),
            ],
            options={
                'verbose_name': 'Discipline',
                'verbose_name_plural': 'Disciplines',
            },
        ),
    ]