from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserProfileExample, Usuario
from datetime import date

class UserProfileExampleTestCase(TestCase):
    
    def setUp(self):
        """Configura o ambiente de teste com um usuário e um perfil"""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.profile = UserProfileExample.objects.create(
            user=self.user,
            phone_number="12345678901",
            address="123 Rua Principal, Pau dos Ferros",
            birth_date=date(1990, 1, 1)
        )

    def test_userprofileexample_creation(self):
        """Testa a criação de um perfil de usuário"""
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.phone_number, "12345678901")
        self.assertEqual(self.profile.address, "123 Rua Principal, Pau dos Ferros")
        self.assertEqual(self.profile.birth_date, date(1990, 1, 1))

    def test_userprofileexample_relationship_with_user(self):
        """Testa a relação entre UserProfileExample e o modelo User"""
        profile = UserProfileExample.objects.get(user=self.user)
        self.assertEqual(profile.user.username, self.user.username)


class UsuarioTestCase(TestCase):
    
    def setUp(self):
        """Configura o ambiente de teste com um usuário e um modelo Usuario"""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.usuario = Usuario.objects.create(
            user=self.user,
            mone="Teste de Mone",
            email="test@example.com",
            senha="testpassword",
            birth_date=date(1990, 1, 1)
        )

    def test_usuario_creation(self):
        """Testa a criação de um objeto Usuario"""
        self.assertEqual(self.usuario.mone, "Teste de Mone")
        self.assertEqual(self.usuario.email, "test@example.com")
        self.assertEqual(self.usuario.senha, "testpassword")
        self.assertEqual(self.usuario.birth_date, date(1990, 1, 1))

    def test_usuario_relationship_with_user(self):
        """Testa a relação entre Usuario e o modelo User"""
        usuario = Usuario.objects.get(user=self.user)
        self.assertEqual(usuario.user.username, self.user.username)

    def test_usuario_email_max_length(self):
        """Testa o comprimento máximo do campo de e-mail"""
        max_length = self.usuario._meta.get_field('email').max_length
        self.assertEqual(max_length, 120)

    def test_usuario_mone_max_length(self):
        """Testa o comprimento máximo do campo 'mone'"""
        max_length = self.usuario._meta.get_field('mone').max_length
        self.assertEqual(max_length, 300)