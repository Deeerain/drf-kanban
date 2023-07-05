from django.contrib.auth import get_user_model

from rest_framework import serializers

from kanban.models import Board, Column, Task


User = get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email')


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('pk', 'name', 'created', 'updated', 'user')


class ColumnSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ('pk', 'title', 'board')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('pk', 'name', 'description', 'updated', 'created', 'user')


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
