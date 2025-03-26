from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from tarefas.models import Tarefa, Categoria, Status
from tarefas.serializer import TarefaSerializer
from django.utils.timezone import localtime

class TarefaSerializerTest(TestCase):
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = User.objects.create_user(username="testuser", password="123456")
        self.categoria = Categoria.objects.create(nome="Estudo")
        self.tarefa = Tarefa.objects.create(
            usuario=self.user,
            titulo="Aprender Django",
            descricao="Estudar Django para o projeto",
            prazo=timezone.now() + timezone.timedelta(days=3),
            prioridade="Média",
            categoria=self.categoria,
            status=Status.PENDENTE
        )

    from django.utils.timezone import localtime

    def test_serializacao_tarefa(self):
        """Verifica se a serialização de uma tarefa ocorre corretamente."""
        serializer = TarefaSerializer(instance=self.tarefa)
        data = serializer.data

        self.assertEqual(data["titulo"], self.tarefa.titulo)
        self.assertEqual(data["descricao"], self.tarefa.descricao)

        self.assertEqual(data["prazo"], localtime(self.tarefa.prazo).isoformat())

        self.assertEqual(data["status"], self.tarefa.status)

    def test_desserializacao_tarefa_valida(self):
        """Verifica se a desserialização de uma tarefa com dados válidos funciona."""
        data = {
            "usuario": self.user.id,
            "titulo": "Nova Tarefa",
            "descricao": "Descrição da nova tarefa",
            "prazo": (timezone.now() + timezone.timedelta(days=2)).isoformat(),
            "prioridade": "Alta",
            "categoria": self.categoria.id,
            "status": Status.PLANEJADA
        }
        serializer = TarefaSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_desserializacao_tarefa_invalida_sem_titulo(self):
        """Verifica se a desserialização falha quando falta o título."""
        data = {
            "usuario": self.user.id,
            "titulo": "",
            "descricao": "Sem título",
            "prazo": (timezone.now() + timezone.timedelta(days=2)).isoformat(),
            "prioridade": "Baixa",
            "categoria": self.categoria.id,
            "status": Status.PENDENTE
        }
        serializer = TarefaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("titulo", serializer.errors)

    def test_desserializacao_tarefa_invalida_sem_prazo(self):
        """Verifica se a desserialização falha quando falta o prazo."""
        data = {
            "usuario": self.user.id,
            "titulo": "Tarefa sem prazo",
            "descricao": "Teste sem prazo",
            "prazo": "",
            "prioridade": "Média",
            "categoria": self.categoria.id,
            "status": Status.PENDENTE
        }
        serializer = TarefaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("prazo", serializer.errors)