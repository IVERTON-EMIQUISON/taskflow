# Generated by Django 4.2.3 on 2025-03-26 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0008_rename_status_arquivamento_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arquivamento',
            old_name='Status',
            new_name='status',
        ),
    ]
