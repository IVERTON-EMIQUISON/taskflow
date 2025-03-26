from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib import admin
from users.api.register_apiview import LoginAPIView, RegistroUsuario
from users.api.views import UserProfileExampleViewSet
from tarefas.views import buscar_tarefa_por_titulo, criar_categoria
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.views.generic import TemplateView

class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_admin_url_resolves(self):
        url = reverse('admin:index')
        self.assertTrue(resolve(url))  # Admin tem resolução dinâmica

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginAPIView)

    def test_schema_url_resolves(self):
        url = reverse('schema')
        self.assertEqual(resolve(url).func.view_class, SpectacularAPIView)

    def test_tarefas_url_resolves(self):
        url = reverse('lista_tarefas') 
        self.assertTrue(resolve(url))

    def test_registro_html_url_resolves(self):
        url = reverse('registro_html')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_criar_categoria_url_resolves(self):
        url = reverse('criar_categoria')
        self.assertEqual(resolve(url).func, criar_categoria)

    def test_registro_usuario_url_resolves(self):
        url = reverse('registro_usuario')
        self.assertEqual(resolve(url).func.view_class, RegistroUsuario)

    def test_swagger_url_resolves(self):
        url = reverse('swagger-ui')
        self.assertEqual(resolve(url).func.view_class, SpectacularSwaggerView)

    def test_buscar_tarefa_por_titulo_url_resolves(self):
        url = reverse('buscar_tarefa_por_titulo', args=['exemplo'])
        self.assertEqual(resolve(url).func, buscar_tarefa_por_titulo)

    def test_lista_url_resolves(self):
        url = reverse('lista')
        self.assertEqual(resolve(url).func.view_class, TemplateView)