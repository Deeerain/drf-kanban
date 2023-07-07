# Generated by Django 4.2.2 on 2023-07-07 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0002_alter_column_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='column',
            options={'ordering': ['position'], 'verbose_name': 'Колонка', 'verbose_name_plural': 'Колонки'},
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(db_index=True, max_length=30, verbose_name='Название'),
        ),
    ]