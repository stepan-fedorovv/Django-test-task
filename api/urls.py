from django.contrib import admin
from django.urls import path
from .views import DirectionMethods, DisciplineMethods, GetCSRFToken, AuthMethods, GroupMethods, StudentMethods, \
    ReportMethods

group_cruds = [
    path('group/', GroupMethods.as_view({"get": "list"})),
    path('group/<int:pk>/', GroupMethods.as_view({"get": "retrieve"})),
    path('group/create/', GroupMethods.as_view({"post": "create"})),
    path('group/<int:pk>/update/', GroupMethods.as_view({"patch": "update"})),
    path('group/<int:pk>/delete/', GroupMethods.as_view({"delete": "destroy"})),
]

student_cruds = [
    path('student/', StudentMethods.as_view({"get": "list"})),
    path('student/<int:pk>/', StudentMethods.as_view({"get": "retrieve"})),
    path('student/create/', StudentMethods.as_view({"post": "create"})),
    path('student/<int:pk>/update/', StudentMethods.as_view({"patch": "update"})),
    path('student/<int:pk>/delete/', StudentMethods.as_view({"delete": "destroy"})),
]

disciplines_cruds = [
    path('disciplines/', DisciplineMethods.as_view({"get": "list"})),
    path('disciplines/<int:pk>/', DisciplineMethods.as_view({"get": "retrieve"})),
    path('disciplines/create/', DisciplineMethods.as_view({"post": "create"})),
    path('disciplines/<int:pk>/update/', DisciplineMethods.as_view({"patch": "update"})),
    path('disciplines/<int:pk>/delete/', DisciplineMethods.as_view({"delete": "destroy"}))
]

direction_cruds = [
    path('directions/', DirectionMethods.as_view({"get": "list"})),
    path('directions/<int:pk>/', DirectionMethods.as_view({"get": "retrieve"})),
    path('directions/create/', DirectionMethods.as_view({"post": "create"})),
    path('directions/<int:pk>/update/', DirectionMethods.as_view({"patch": "update"})),
    path('directions/<int:pk>/delete/', DirectionMethods.as_view({"delete": "destroy"})),
]

auth_curds = [
    path('csrf/', GetCSRFToken.as_view({"get": "get_cookie"})),
    path('registration/', AuthMethods.as_view({"post": "register_user"})),
    path('login/', AuthMethods.as_view({"post": "sing_in"})),
    path('logout/', AuthMethods.as_view({"post": "logout_user"}))
]

report_methods = [
    path('report/generate/', ReportMethods.as_view({"get": "generate"})),
    path('report/status/', ReportMethods.as_view({"get": "report_generate_status"}))
]

urlpatterns = []

urlpatterns += direction_cruds
urlpatterns += disciplines_cruds
urlpatterns += auth_curds
urlpatterns += group_cruds
urlpatterns += student_cruds
urlpatterns += report_methods
