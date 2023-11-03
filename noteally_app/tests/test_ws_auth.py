from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock
from django.urls import reverse
from noteally_app.models import User
from noteally_app.webservices.ws_auth import get_cognito_user


@patch('noteally_app.webservices.ws_auth.requests')
class TestAuthView(APITestCase):
    
    def setUp(self):
        self.url = reverse('login')

    def test_get_cognito_user_success(self, mock_requests):

        # mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "sub": "0123456789",
            "email_verified": True,
            "given_name": "John",
            "family_name": "Doe",
            "email": "johndoe@gmail.com",
            "username": "0123456789"
        }

        # mock requests.get
        mock_requests.get.return_value = mock_response

        # call get_cognito_user
        access_token = "0123456789"
        return_value = get_cognito_user(access_token)

        # assert the response
        self.assertEqual(return_value['sub'], '0123456789')
        self.assertEqual(return_value['email_verified'], True)
        self.assertEqual(return_value['first_name'], 'John')
        self.assertEqual(return_value['last_name'], 'Doe')
        self.assertEqual(return_value['email'], 'johndoe@gmail.com')
        self.assertEqual(return_value['username'], '0123456789')
        

    def test_get_cognito_user_error(self, mock_requests):

            # mock response
            mock_response = MagicMock()
            mock_response.status_code = 401
            mock_response.json.return_value = {
                "error": "invalid_token",
                "error_description": "Access token format is not valid"
            }

            # mock requests.get
            mock_requests.get.return_value = mock_response

            # call get_cognito_user
            access_token = "0123456789"
            return_value = get_cognito_user(access_token)

            # assert the response
            self.assertEqual(return_value, None)


    def test_register_success(self, mock_requests):

        # mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "sub": "0123456789",
            "email_verified": True,
            "given_name": "John",
            "family_name": "Doe",
            "email": "johndoe@gmail.com",
            "username": "0123456789"
        }

        # mock requests.get
        mock_requests.get.return_value = mock_response

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


    def test_login_success(self, mock_requests):

        # mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "sub": "0123456789",
            "email_verified": True,
            "given_name": "John",
            "family_name": "Doe",
            "email": "johndoe@gmail.com",
            "username": "0123456789"
        }

        # mock requests.get
        mock_requests.get.return_value = mock_response

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


    def test_register_error(self, mock_requests):

        # mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": "invalid_token",
            "error_description": "Access token format is not valid"
        }

        # mock requests.get
        mock_requests.get.return_value = mock_response

        data = {
            "id_token": "123",
            "access_token": "123"
        }
        response = self.client.post(self.url, data, format='multipart')

        # Assert the response status code
        self.assertEqual(response.status_code, 400)
