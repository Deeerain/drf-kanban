from django.contrib.auth import get_user_model, login

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.status import HTTP_201_CREATED
from rest_framework.decorators import action
from rest_framework.response import Response

from kanban.serializers import (
    BoardSerializer, ColumnSeriaizer, TaskSerializer, UserSerializer,
    RegistrationSerializer)
from kanban.models import Board, Column, Task


User = get_user_model()


class BoardViewset(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [
        permissions.IsAdminUser,
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return Board.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ColumnViewset(viewsets.ModelViewSet):
    serializer_class = ColumnSeriaizer
    filterset_fields = ['board']
    permission_classes = [
        permissions.IsAdminUser,
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        last_column = self.get_queryset().last()
        serializer.save(position=last_column.position + 1)

    def get_queryset(self):
        return Column.objects.filter(board__user=self.request.user)


class TaskViewset(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filterset_fields = ['column']
    permission_classes = [
        permissions.IsAdminUser,
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return Task.objects.filter(column__board__user=self.request.user)

    def perform_create(self, serializer):
        last_task = self.get_queryset().last()
        return serializer.save(
            user=self.request.user, position=last_task.position + 1)


class UserViewset(viewsets.ViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        return self.request.user

    @action(['GET', 'PUT'], detail=False, url_path='me')
    def get_me(self, request):
        user = User.objects.get(pk=request.user.pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    @action(['POST'], detail=False, url_path='register')
    def register(self, request):
        serializer = RegistrationSerializer(request.POST)
        user = serializer.save()
        login(request, user)
        return Response(serializer.data, status=HTTP_201_CREATED)
