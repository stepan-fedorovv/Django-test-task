from celery import result
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import (
    status,
    permissions,
    authentication,
    mixins,
    viewsets,
    generics,
)
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .models import Direction, Discipline, Group, Student, CustomUser
from .seriazliers import (
    DirectionSerializer,
    DisciplineSerializer,
    StudentSerializer,
    GroupSerializer,
    RegistrationSerializer,
    LoginSerializer,
)
from .permissions import IsCuratorUser
from .tasks import generate_report


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFToken(viewsets.GenericViewSet):
    permission_classes = [
        permissions.AllowAny,
    ]

    @staticmethod
    def get_cookie(self):
        return Response({"success": "CSRF Token Set"})


@method_decorator(csrf_protect, name="dispatch")
class AuthMethods(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    registration_serializer = RegistrationSerializer
    login_serializer = LoginSerializer
    queryset = CustomUser.objects.all()

    def register_user(self, request, *args, **kwargs):
        self.serializer_class = self.registration_serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = auth.authenticate(
            request,
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if user is None:
            return Response({"detail": "User invalid"})
        auth.login(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def sing_in(self, request):
        self.serializer_class = self.login_serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = auth.authenticate(
            request,
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if user is not None:
            if user.is_active:
                auth.login(request, user)
        else:
            return Response("Invalid username or password")
        return Response(
            {"email": user.email, "username": user.username}, status=status.HTTP_200_OK
        )

    @staticmethod
    def logout_user(request):
        auth.logout(request)
        return Response({"status": "success"}, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name="dispatch")
class DirectionMethods(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = DirectionSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    queryset = Direction.objects.all()
    permission_classes = [
        permissions.IsAdminUser,
    ]

    def get_object(self):
        pk = self.kwargs.get("pk")
        direction = generics.get_object_or_404(Direction, pk=pk)
        return direction


@method_decorator(csrf_protect, name="dispatch")
class DisciplineMethods(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = DisciplineSerializer
    permission_classes = [
        permissions.IsAdminUser,
    ]
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    queryset = Discipline.objects.all()

    def get_object(self):
        pk = self.kwargs.get("pk")
        discipline = generics.get_object_or_404(Discipline, pk=pk)
        return discipline


@method_decorator(csrf_protect, name="dispatch")
class StudentMethods(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = StudentSerializer
    permission_classes = [
        IsCuratorUser,
    ]
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    queryset = Student.objects.all()

    def get_object(self):
        pk = self.kwargs.get("pk")
        student = generics.get_object_or_404(Student, pk=pk)
        return student


@method_decorator(csrf_protect, name="dispatch")
class GroupMethods(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = GroupSerializer
    permission_classes = [
        IsCuratorUser,
    ]
    authentication_classes = [
        authentication.SessionAuthentication,
    ]
    queryset = Group.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(curator=self.request.user)
        if queryset.count() > 20:
            raise ValidationError({"detail": "Group is full"})
        return queryset

    def get_object(self):
        pk = self.kwargs.get("pk")
        group = generics.get_object_or_404(Group, pk=pk)
        return group


class ReportMethods(viewsets.GenericViewSet):
    @staticmethod
    def generate(request):
        celery_task = generate_report.delay()
        return Response(
            {
                "task_status": f"{result.AsyncResult(celery_task).state}",
                "task_id": f"{result.AsyncResult(celery_task)}",
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def report_generate_status(request):
        task_id = request.query_params.get("task_id")
        try:
            task_status = result.AsyncResult(task_id).status
            return Response({"status": task_status})
        except ValueError:
            return Response({"detail": "Invalid task id"})
