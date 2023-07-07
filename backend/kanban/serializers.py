from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from rest_framework import serializers

from kanban.models import Board, Column, Task


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email')


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('pk', 'name', 'created', 'updated')


class ColumnSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ('pk', 'title', 'board', 'position')

    def create(self, validated_data):
        board = validated_data.get('board')
        queryset = Column.objects.filter(board=board)
        return create_positionable_element(queryset, **validated_data)


class CreateColumnSeriaizer(ColumnSeriaizer):
    class Meta:
        model = Column
        fields = ('pk', 'title', 'board')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('pk', 'name', 'description', 'updated',
                  'created', 'user', 'position')

    def create(self, validated_data):
        column = validated_data.get('column')
        queryset = Task.objects.filter(column=column)
        return create_positionable_element(queryset, **validated_data)


class CreateTaskSerializer(TaskSerializer):
    class Meta:
        model = Task
        fields = ('pk', 'name', 'description', 'column')


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        user = User()
        user.username = validated_data.get('username')
        user.email = validated_data.get('email')
        user.set_password(validated_data.get('password'))
        return user


# TODO Убрать в отдельный файл
def create_positionable_element(queryset: QuerySet, **kwargs):
    position = 0

    if last_element := queryset.last():
        position = last_element.position + 1

    kwargs.setdefault('position', position)

    return queryset.create(**kwargs)
