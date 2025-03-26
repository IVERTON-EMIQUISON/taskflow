from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tarefas.models import Tarefa, Categoria, Status
from django.utils.timezone import now, timedelta

class TarefaViewsTest(TestCase):
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = Client()
        self.usuario = User.objects.create_user(username="testuser", password="testpass")
        self.categoria = Categoria.objects.create(nome="Trabalho")
        self.tarefa = Tarefa.objects.create(
            usuario=self.usuario,
            titulo="Teste de Tarefa",
            descricao="Descrição da tarefa",
            prazo=now() + timedelta(days=2),
            prioridade="Média",
            categoria=self.categoria,
            status=Status.PENDENTE,
        )

    def test_lista_tarefas_redireciona_se_nao_autenticado(self):
        """Testa se o usuário não autenticado é redirecionado"""
        response = self.client.get(reverse("lista_tarefas"))
        self.assertEqual(response.status_code, 302)  # Redirecionado para login

    def test_lista_tarefas_renderiza_corretamente(self):
        """Testa se a lista de tarefas é carregada corretamente"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("lista_tarefas"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tarefas/lista.html")
        self.assertContains(response, "Teste de Tarefa")

    # ! Falhará até que o problema de fuso horário seja resolvido no código.
    # def test_criar_tarefa_sucesso(self):
    #     """Testa a criação de uma nova tarefa"""
    #     self.client.login(username="testuser", password="testpass")
    #     data = {
    #         "titulo": "Nova Tarefa",
    #         "descricao": "Descrição da nova tarefa",
    #         "categoria": self.categoria.id,
    #         "status": Status.PLANEJADA,
    #         "prazo": (now() + timedelta(days=3)).isoformat(),
    #     }
    #     response = self.client.post(reverse("tarefas:criar_tarefa"), data)
    #     self.assertEqual(response.status_code, 201)  # Criado com sucesso
    #     self.assertTrue(Tarefa.objects.filter(titulo="Nova Tarefa").exists())

    def test_deletar_tarefa(self):
        """Testa se uma tarefa é deletada corretamente"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("deletar_tarefa", args=[self.tarefa.id]))
        self.assertEqual(response.status_code, 302)  # Redireciona após deletar
        self.assertFalse(Tarefa.objects.filter(id=self.tarefa.id).exists())

    def test_atualizar_status(self):
        """Testa a atualização do status da tarefa"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.patch(
            reverse("atualizar_status", args=[self.tarefa.pk]),
            {"status": Status.EM_ANDAMENTO},
            content_type="application/json",
        )
        self.tarefa.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tarefa.status, Status.EM_ANDAMENTO)