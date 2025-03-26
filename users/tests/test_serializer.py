from django.test import TestCase
from users.models import UserProfileExample, User
from users.api.serializers import UserProfileExampleSerializer
from datetime import date

class UserProfileExampleSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.user_profile = UserProfileExample.objects.create(
            user=self.user,
            address="123 Test St",
            phone_number="1234567890",
            birth_date=date(1995, 5, 15)
        )

        self.valid_data = {
            'user': self.user.id,
            'address': "456 New St",
            'phone_number': "0987654321",
            'birth_date': "2000-01-01"
        }

        self.invalid_data = {
            'address': "789 Error St",
            'phone_number': "1112223333",
            # 'birth_date' está faltando
            'user': self.user.id
        }

    def test_serializer_valid_data(self):
      """Testa se o serializador aceita dados válidos."""
      new_user = User.objects.create_user(username='newtestuser', password='testpassword')
      valid_data = {
        'user': new_user.id,
        'address': "456 New St",
        'phone_number': "0987654321",
        'birth_date': "2000-01-01"
      }
      serializer = UserProfileExampleSerializer(data=valid_data)
      self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_invalid_data(self):
        """Testa se o serializador rejeita dados inválidos."""
        serializer = UserProfileExampleSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('birth_date', serializer.errors)  

    def test_serializer_serialization(self):
        """Testa se o serializador converte corretamente o objeto para JSON."""
        serializer = UserProfileExampleSerializer(instance=self.user_profile)
        expected_data = {
            'id': self.user_profile.id,
            'user': self.user.id,
            'address': self.user_profile.address,
            'phone_number': self.user_profile.phone_number,
            'birth_date': str(self.user_profile.birth_date)
        }
        self.assertEqual(serializer.data, expected_data)