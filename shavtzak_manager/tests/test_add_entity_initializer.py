from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import UserSystemCustomFields, UserType

class AddEntityInitializerViewTests(APITestCase):

    def setUp(self):
        self.url = reverse('add_entity_initializer')
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.invalid_data = {
            'username': '',
            'email': 'invalid-email',
            'password': '',
            'first_name': '',
            'last_name': ''
        }

    def test_create_entity_initializer_success(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('user_id', response.data)
        self.assertIn('email', response.data)
        
        # Check if the user exists in the database
        user = User.objects.get(username=self.valid_data.get("username"))
        self.assertEqual(user.email, self.valid_data.get("email"))

        # Check if the user is set as an entity initializer
        custom_fields = UserSystemCustomFields.objects.get(user=user)
        self.assertEqual(custom_fields.user_type, UserType.ENTITY_INITIALIZER.value)

    def test_create_entity_initializer_invalid_data(self):
        response = self.client.post(self.url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)

        user = User.objects.filter(username=self.invalid_data.get("username"))
        self.assertFalse(user.exists())
