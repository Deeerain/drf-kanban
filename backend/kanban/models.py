from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Board(models.Model):
    '''
    Модель доски
    '''
    name = models.CharField(
        verbose_name=_('Название'), max_length=30,
        db_index=True, unique=True)
    user = models.ForeignKey(
        verbose_name=_('Пользователь'), to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(
        verbose_name=_('Дата создания'), auto_now_add=True)
    updated = models.DateTimeField(
        verbose_name=_('Дата обновления'), auto_now=True, db_index=True)

    class Meta:
        verbose_name = _('Доска')
        verbose_name_plural = _('Доски')

    def __str__(self) -> str:
        return self.name


class Column(models.Model):
    '''Модель колонки доски'''
    title = models.CharField(
        verbose_name=_('Название'), max_length=30, db_index=True)
    board = models.ForeignKey(
        verbose_name=_('Доска'), to=Board, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(
        verbose_name=_('Позиция'))

    class Meta:
        verbose_name = _('Колонка')
        verbose_name_plural = _('Колонки')

    def __str__(self) -> str:
        return self.title


class Task(models.Model):
    '''
    Модель задачи
    '''
    name = models.CharField(
        verbose_name=_('Название'), max_length=30, db_index=True)
    description = models.TextField(
        verbose_name=_('Описание'))
    position = models.PositiveIntegerField(
        verbose_name=_('Позиция'))
    column = models.ForeignKey(
        verbose_name=_('Колонка'), to=Column, on_delete=models.CASCADE)
    user = models.ForeignKey(
        verbose_name=_('Пользователь'), to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(
        verbose_name=_('Дата создания'), auto_now_add=True)
    updated = models.DateTimeField(
        verbose_name=_('Дата обновления'), auto_now=True, db_index=True)

    class Meta:
        verbose_name = _('Задача')
        verbose_name_plural = _('Задачи')
        ordering = ['position']

    def __str__(self) -> str:
        self.name
