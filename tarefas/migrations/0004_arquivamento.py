# Generated by Django 4.2.3 on 2025-03-13 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tarefas', '0003_alter_tarefa_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arquivamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivada', models.BooleanField(default=True)),
                ('data_arquivamento', models.DateTimeField(auto_now_add=True)),
                ('tarefa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tarefas.tarefa')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
