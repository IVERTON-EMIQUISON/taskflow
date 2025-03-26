from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from tarefas.forms import TarefaForm, CategoriaForm
from tarefas.models import Categoria, Tarefa, Status

class TarefaFormTest(TestCase):
    def setUp(self):
        """Cria um usuário e uma categoria para serem usados nos testes."""
        self.user = User.objects.create_user(username="testuser", password="123456")
        self.categoria = Categoria.objects.create(nome="Trabalho")

    def test_tarefa_form_valido(self):
        """Verifica se o formulário é válido com dados corretos."""
        form_data = {
            'titulo': 'Estudar Django',
            'descricao': 'Aprender a criar projetos com Django',
            'categoria': self.categoria.id,
            'status': Status.PENDENTE,
            'prazo': (timezone.now() + timezone.timedelta(days=3)).isoformat()
        }
        form = TarefaForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_tarefa_form_invalido_sem_titulo(self):
        """Verifica se o formulário é inválido sem título."""
        form_data = {
            'titulo': '',
            'descricao': 'Descrição válida',
            'categoria': self.categoria.id,
            'status': Status.PENDENTE,
            'prazo': (timezone.now() + timezone.timedelta(days=3)).isoformat()
        }
        form = TarefaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors) 

    def test_tarefa_form_invalido_sem_prazo(self):
        """Verifica se o formulário é inválido sem prazo."""
        form_data = {
            'titulo': 'Tarefa sem prazo',
            'descricao': 'Teste sem prazo',
            'categoria': self.categoria.id,
            'status': Status.PENDENTE,
            'prazo': ''
        }
        form = TarefaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('prazo', form.errors) 


class CategoriaFormTest(TestCase):
    def test_categoria_form_valido(self):
        """Verifica se o formulário de categoria é válido."""
        form_data = {'nome': 'Lazer'}
        form = CategoriaForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_categoria_form_invalido_sem_nome(self):
        """Verifica se o formulário de categoria é inválido sem nome."""
        form_data = {'nome': ''}
        form = CategoriaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)  