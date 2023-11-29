from django.contrib import admin
from django.urls import path
from .views import DirectionMethods, DisciplineMethods

urlpatterns = [
    path('directions/', DirectionMethods.as_view({"get": "list"})),
    path('directions/<int:pk>/', DirectionMethods.as_view({"get": "retrieve"})),
    path('directions/create/', DirectionMethods.as_view({"post": "create"})),
    path('directions/<int:pk>/update/', DirectionMethods.as_view({"patch": "update"})),
    path('directions/<int:pk>/delete/', DirectionMethods.as_view({"delete": "destroy"})),
    path('disciplines/', DisciplineMethods.as_view({"get": "list"})),
    path('disciplines/<int:pk>/', DisciplineMethods.as_view({"get": "retrieve"})),
    path('disciplines/create/', DisciplineMethods.as_view({"post": "create"})),
    path('disciplines/<int:pk>/update/', DisciplineMethods.as_view({"patch": "update"})),
    path('disciplines/<int:pk>/delete', DisciplineMethods.as_view({"delete": "destroy"}))
]
