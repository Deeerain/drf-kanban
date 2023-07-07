from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from kanban.serializers import (
    BoardSerializer, ColumnSeriaizer, CreateColumnSeriaizer, TaskSerializer,
    CreateTaskSerializer, UserSerializer)

from kanban.models import Board, Column, Task


User = get_user_model()


class BoardViewset(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [
        permissions.IsAdminUser,
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return Board.objects.filter(user=self.request.user)


class ColumnViewset(viewsets.ModelViewSet):
    serializer_class = ColumnSeriaizer
    filterset_fields = ['board']
    permission_classes = [
        permissions.IsAdminUser,
        permissions.IsAuthenticated,
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateColumnSeriaizer

        return super().get_serializer_class()

    def perform_destroy(self, instance):
        queryset = self.get_queryset().filter(board=instance.board)
        arrange_positionable_elements(queryset)
        return super().perform_destroy(instance)

    def get_queryset(self):
        return Column.objects.filter(board__user=self.request.user)


class TaskViewset(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filterset_fields = ['column']
    permission_classes = [
        permissions.IsAdminUser,
        permissions.IsAuthenticated,
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTaskSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        return Task.objects.filter(column__board__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

        queryset = self.get_queryset().\
            filter(column=instance.column)

        arrange_positionable_elements(queryset)


class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    @action(['GET'], detail=False)
    def me(self, request):
        user = self.get_queryset().get(pk=request.user.pk)
        serializer = self.get_serializer(user)
        print(serializer.data)
        return Response(serializer.data)


# TODO Убрать в отдельный файл
@transaction.atomic
def arrange_positionable_elements(queryset: QuerySet):
    with transaction.atomic():
        for index, element in enumerate(queryset):
            if element.position == index:
                continue
            element.position = index
            element.save()
