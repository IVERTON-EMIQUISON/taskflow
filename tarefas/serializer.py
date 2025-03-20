# Description: Serializers for the tarefas app.
from rest_framework import serializers
from tarefas.models import Tarefa, Categoria
from django.contrib.auth.models import User

class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = '__all__'
