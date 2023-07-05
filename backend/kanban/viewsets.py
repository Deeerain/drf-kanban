from rest_framework import viewsets

from kanban.serializers import BoardSerializer, ColumnSeriaizer, TaskSerializer
from kanban.models import Board, Column, Task


class BoardViewset(viewsets.ModelViewSet):
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ColumnViewset(viewsets.ModelViewSet):
    serializer_class = ColumnSeriaizer

    def get_queryset(self):
        return Column.objects.all()

    def filter_queryset(self, queryset):
        board_id = self.request.GET.get('board_id')

        if board_id is None:
            raise ValueError('board_id is none')

        return queryset.filter(board__user=self.request.user, board=board_id)


class TaskViewset(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
