from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class RegistroUsuarioTestCase(APITestCase):

    def setUp(self):
        self.existing_user = User.objects.create_user(username="existinguser", password="testpassword", email="existing@example.com")
        self.url = reverse('registro_usuario')  

    def test_registro_sucesso(self):
        """Testa se um usuário é registrado com sucesso"""
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")
        self.assertEqual(response.data["email"], "newuser@example.com")
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_registro_usuario_existente(self):
        """Testa se a API impede a criação de um usuário já existente"""
        data = {
            "username": "existinguser",
            "password": "anotherpassword",
            "email": "newemail@example.com"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Este nome de usuário já está em uso")

    def test_registro_campos_faltando(self):
        """Testa se a API retorna erro quando campos obrigatórios estão ausentes"""
        data = {
            "username": "usersememail",
            "password": "password123"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Nome de usuário, senha e e-mail são necessários")
