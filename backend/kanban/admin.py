from django.contrib import admin

from kanban import models


@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')


@admin.register(models.Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')
