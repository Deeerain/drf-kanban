from rest_framework import viewsets

from kanban.serializers import BoardSerializer, ColumnSeriaizer, TaskSerializer
from kanban.models import Board, Column, Task


class BoardViewset(viewsets.ModelViewSet):
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ColumnViewset(viewsets.ModelViewSet):
    serializer_class = ColumnSeriaizer
    filterset_fields = ['board']

    def perform_create(self, serializer):
        last_column = self.get_queryset().last()
        serializer.save(position=last_column.position + 1)

    def get_queryset(self):
        return Column.objects.filter(board__user=self.request.user)


class TaskViewset(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filterset_fields = ['column']

    def get_queryset(self):
        return Task.objects.filter(column__board__user=self.request.user)

    def perform_create(self, serializer):
        last_task = self.get_queryset().last()
        return serializer.save(
            user=self.request.user, position=last_task.position + 1)
