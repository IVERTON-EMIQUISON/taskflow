from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from tarefas.models import Categoria, Tarefa, Arquivamento, Status

class CategoriaModelTest(TestCase):
    def test_criacao_categoria(self):
        """Verifica se uma categoria pode ser criada corretamente."""
        categoria = Categoria.objects.create(nome="Trabalho")
        self.assertEqual(categoria.nome, "Trabalho")

    def test_categoria_str(self):
        """Verifica se a representação textual da categoria está correta."""
        categoria = Categoria.objects.create(nome="Estudos")
        self.assertEqual(str(categoria), "Estudos")


class TarefaModelTest(TestCase):
    def setUp(self):
        """Configuração inicial antes dos testes."""
        self.user = User.objects.create_user(username="testuser", password="123456")
        self.categoria = Categoria.objects.create(nome="Pessoal")
        self.tarefa = Tarefa.objects.create(
            usuario=self.user,
            titulo="Finalizar relatório",
            descricao="Escrever a conclusão do relatório",
            prazo=timezone.now() + timezone.timedelta(days=2),
            prioridade="Alta",
            categoria=self.categoria,
            concluida=False,
            status=Status.PENDENTE
        )

    def test_criacao_tarefa(self):
        """Verifica se uma tarefa pode ser criada corretamente."""
        self.assertEqual(self.tarefa.titulo, "Finalizar relatório")
        self.assertEqual(self.tarefa.status, Status.PENDENTE)
        self.assertFalse(self.tarefa.concluida)

    def test_tarefa_str(self):
        """Verifica se a representação textual da tarefa está correta."""
        self.assertEqual(str(self.tarefa), "Finalizar relatório")

    def test_tarefa_atrasada(self):
        """Verifica se a função 'atrasada' retorna corretamente se a tarefa passou do prazo."""
        self.tarefa.prazo = timezone.now() - timezone.timedelta(days=1)  
        self.assertTrue(self.tarefa.atrasada())

        self.tarefa.prazo = timezone.now() + timezone.timedelta(days=1)  
        self.assertFalse(self.tarefa.atrasada())

    def test_concluir_tarefa(self):
        """Verifica se a tarefa é concluída e arquivada corretamente."""
        self.tarefa.status = Status.CONCLUIDA
        self.tarefa.concluir_tarefa()

        self.tarefa.refresh_from_db()
        self.assertTrue(self.tarefa.concluida)

        arquivamento = Arquivamento.objects.filter(tarefa=self.tarefa).first()
        self.assertIsNotNone(arquivamento)
        self.assertEqual(arquivamento.usuario, self.tarefa.usuario)


class ArquivamentoModelTest(TestCase):
    def setUp(self):
        """Configuração inicial antes dos testes."""
        self.user = User.objects.create_user(username="testuser", password="123456")
        self.tarefa = Tarefa.objects.create(
            usuario=self.user,
            titulo="Estudar para prova",
            prazo=timezone.now() + timezone.timedelta(days=3),
            prioridade="Média",
            categoria=None,
            concluida=True,
            status=Status.CONCLUIDA
        )
        self.arquivamento = Arquivamento.objects.create(usuario=self.user, tarefa=self.tarefa)

    def test_criacao_arquivamento(self):
        """Verifica se um arquivamento pode ser criado corretamente."""
        self.assertEqual(self.arquivamento.usuario, self.user)
        self.assertEqual(self.arquivamento.tarefa, self.tarefa)
        self.assertEqual(self.arquivamento.Status, Status.CONCLUIDA)