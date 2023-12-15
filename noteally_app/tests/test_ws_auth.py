from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock
from django.urls import reverse
from noteally_app.models import User
from noteally_app.webservices.ws_auth import get_cognito_user
from noteally_app.models import StudyArea


@patch('noteally_app.decorators.requests')
class TestAuthView(APITestCase):
    
    def setUp(self):
        self.study_area1 = StudyArea.objects.create(name="Computer Science")
        self.url = reverse('login')

        # user basic info
        self.user_id = 1
        self.user_sub = "0123456789"
        self.user_fname = "John"
        self.user_lname = "Doe"
        self.user_email = "johndoe@gmail.com"
        self.access_token = "0123456789"

        # mock success response from cognito
        self.mock_success_response = MagicMock()
        self.mock_success_response.status_code = 200
        self.mock_success_response.json.return_value = {
            "sub": "0123456789",
            "email_verified": True,
            "given_name": "John",
            "family_name": "Doe",
            "email": "johndoe@gmail.com",
            "username": "0123456789"
        }

        # mock error response from cognito
        self.mock_error_response = MagicMock()
        self.mock_error_response.status_code = 401
        self.mock_error_response.json.return_value = {
            "error": "invalid_token",
            "error_description": "Access token format is not valid"
        }


    def test_get_cognito_user_success(self, mock_requests):

        # mock requests.get
        mock_requests.get.return_value = self.mock_success_response

        # call get_cognito_user
        return_value = get_cognito_user(self.access_token)

        # assert the response
        self.assertEqual(return_value['sub'], self.user_sub)
        self.assertEqual(return_value['email_verified'], True)
        self.assertEqual(return_value['first_name'], self.user_fname)
        self.assertEqual(return_value['last_name'], self.user_lname)
        self.assertEqual(return_value['email'], self.user_email)
        

    def test_get_cognito_user_error(self, mock_requests):

            # mock requests.get
            mock_requests.get.return_value = self.mock_error_response

            # call get_cognito_user
            return_value = get_cognito_user(self.access_token)

            # assert the response
            self.assertEqual(return_value, None)


    def test_register_success(self, mock_requests):

        # mock requests.get
        mock_requests.get.return_value = self.mock_success_response

        data = {
            "id_token": "0123456789",
            "access_token": "0123456789"
        }
        response = self.client.post(self.url, data, format='multipart')

        excepted_response = {
            'id': self.user_id,
            'sub': self.user_sub,
            'id_token': data['id_token'],
            'first_name': self.user_fname,
            'last_name': self.user_lname,
            'email': self.user_email,
            'premium': False,
            'karma_score': 0,
            'tutoring_services': False,
            'profile_picture': None,
            'registered': False,
            'description': '', 
            'study_areas': []
        }

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the response data
        self.assertEqual(response.data, excepted_response)


    def test_login_success(self, mock_requests):

        # mock requests.get
        mock_requests.get.return_value = self.mock_success_response

        # Register user in database
        user1 = User(
            sub = self.user_sub,
            first_name = self.user_fname,
            last_name = self.user_lname,
            email = self.user_email
        )
        user1.save()

        data = {
            "id_token": "0123456789",
            "access_token": "0123456789"
        }
        response = self.client.post(self.url, data, format='multipart')

        excepted_response = {
            'id': self.user_id,
            'sub': self.user_sub,
            'id_token': data['id_token'],
            'first_name': self.user_fname,
            'last_name': self.user_lname,
            'email': self.user_email,
            'premium': False,
            'karma_score': 0,
            'tutoring_services': False,
            'profile_picture': None,
            'registered': True,
            'description': '', 
            'study_areas': []
        }

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the response data
        self.assertEqual(response.data, excepted_response)


    def test_register_error(self, mock_requests):

        # mock requests.get
        mock_requests.get.return_value = self.mock_error_response

        data = {
            "id_token": "123",
            "access_token": "123"
        }
        response = self.client.post(self.url, data, format='multipart')

        # Assert the response status code
        self.assertEqual(response.status_code, 400)
