from celery.app import task
from celery.result import AsyncResult
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .models import Direction, Discipline, Group, Student, CustomUser
from .seriazliers import DirectionSerializer, DisciplineSerializer, StudentSerializer, GroupSerializer, \
    RegistrationSerializer, LoginSerializer
from .permissions import IsCuratorUser
from .tasks import generate_report


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(GenericViewSet):
    permission_classes = [AllowAny, ]

    @staticmethod
    def get_cookie(self):
        return Response({"success": "CSRF Token Set"})


@method_decorator(csrf_protect, name='dispatch')
class AuthMethods(GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin):
    authentication_classes = [SessionAuthentication, ]
    registration_serializer = RegistrationSerializer
    login_serializer = LoginSerializer
    queryset = CustomUser.objects.all()

    def register_user(self, request, *args, **kwargs):
        self.serializer_class = self.registration_serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))
        if user is None:
            return Response({"detail": "User invalid"})
        login(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def sing_in(self, request):
        self.serializer_class = self.login_serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))
        if user is not None:
            if user.is_active:
                login(request, user)
        else:
            return Response("Invalid username or password")
        return Response({"email": user.email, "username": user.username}, status=status.HTTP_200_OK)

    @staticmethod
    def logout_user(request):
        logout(request)
        return Response({"status": "success"}, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name='dispatch')
class DirectionMethods(GenericViewSet,
                       mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin):
    serializer_class = DirectionSerializer
    authentication_classes = [SessionAuthentication, ]
    queryset = Direction.objects.all()
    permission_classes = [IsAdminUser, ]

    def get_object(self):
        pk = self.kwargs.get('pk')
        direction = get_object_or_404(Direction, pk=pk)
        return direction

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_object()
        self.perform_destroy(queryset)
        return Response({"status": "deleted"}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = self.get_object()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


@method_decorator(csrf_protect, name='dispatch')
class DisciplineMethods(GenericViewSet,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin):
    serializer_class = DisciplineSerializer
    permission_classes = [IsAdminUser, ]
    authentication_classes = [SessionAuthentication, ]
    queryset = Discipline.objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk')
        discipline = get_object_or_404(Discipline, pk=pk)
        return discipline

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_object()
        self.perform_destroy(queryset)
        return Response({"status": "deleted"}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = self.get_object()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name='dispatch')
class StudentMethods(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin):
    serializer_class = StudentSerializer
    permission_classes = [IsCuratorUser, ]
    authentication_classes = [SessionAuthentication, ]
    queryset = Student.objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk')
        student = get_object_or_404(Student, pk=pk)
        return student

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_object()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_object()
        self.perform_destroy(queryset)
        return Response({"status": "deleted"}, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name='dispatch')
class GroupMethods(GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin):
    serializer_class = GroupSerializer
    permission_classes = [IsCuratorUser, ]
    authentication_classes = [SessionAuthentication, ]
    queryset = Group.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(curator=self.request.user)
        if queryset.count() > 20:
            raise ValidationError({"detail": "Group is full"})
        return queryset

    def get_object(self):
        pk = self.kwargs.get('pk')
        group = get_object_or_404(Group, pk=pk)
        return group

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = self.get_serializer(instance=queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = self.get_object()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_object()
        self.perform_destroy(queryset)
        return Response({"status": "deleted"}, status=status.HTTP_200_OK)


class ReportMethods(GenericViewSet):
    discipline_queryset = Discipline.objects.prefetch_related('direction')

    def get_discipline_queryset(self):
        queryset = self.discipline_queryset
        return queryset

    @staticmethod
    def generate(request):
        celery_task = generate_report.delay()
        return Response({"task_status": f"{AsyncResult(celery_task).state}", "task_id": f"{AsyncResult(celery_task)}"},
                        status=status.HTTP_200_OK)

    @staticmethod
    def report_generate_status(request):
        task_id = request.query_params.get('task_id')
        try:
            task_status = AsyncResult(task_id).status
            return Response({"status": task_status})
        except ValueError:
            return Response({"detail": "Invalid task id"})


