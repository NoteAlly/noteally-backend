from rest_framework.test import APITestCase
from unittest.mock import patch
from django.urls import reverse
from noteally_app.models import User


def get_cognito_user_mock(access_token):
    if len(access_token) < 10:
        return None
    return {
        'sub': '0123456789',
        'email_verified': True,
        'email_verified': True,
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@gmail.com',
        'username': 'johndoe'
    }


@patch('noteally_app.webservices.ws_auth.get_cognito_user', side_effect=get_cognito_user_mock)
class TestAuthView(APITestCase):
    
    def setUp(self):
        self.url = reverse('login')


    def test_register_success(self, user):
        data = {
            "id_token": "0123456789",
            "access_token": "0123456789"
        }
        response = self.client.post(self.url, data, format='multipart')

        excepted_response = {
            'id': 1,
            'sub': '0123456789',
            'id_token': '0123456789',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@gmail.com',
            'premium': False,
            'karma_score': 0,
            'tutoring_services': False,
            'profile_picture': None,
            'registered': False
        }

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the response data
        self.assertEqual(response.data, excepted_response)


    def test_login_success(self, user):
        # Register user in database
        user1 = User(
            sub="0123456789",
            first_name="John",
            last_name="Doe",
            email="johndoe@gmail.com"
        )
        user1.save()

        data = {
            "id_token": "0123456789",
            "access_token": "0123456789"
        }
        response = self.client.post(self.url, data, format='multipart')

        excepted_response = {
            'id': 1,
            'sub': '0123456789',
            'id_token': '0123456789',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@gmail.com',
            'premium': False,
            'karma_score': 0,
            'tutoring_services': False,
            'profile_picture': None,
            'registered': True
        }

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the response data
        self.assertEqual(response.data, excepted_response)


    def test_register_error(self, user):
        data = {
            "id_token": "123",
            "access_token": "123"
        }
        response = self.client.post(self.url, data, format='multipart')

        # Assert the response status code
        self.assertEqual(response.status_code, 400)
