from django.contrib.auth import get_user_model

from rest_framework import serializers

from kanban.models import Board, Column, Task


User = get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('pk', 'name', 'created', 'updated', 'user')


class ColumnSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ('pk', 'name', 'board', 'created', 'updated')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('pk', 'name', 'description', 'updated', 'created', 'user')
