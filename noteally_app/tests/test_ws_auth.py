from rest_framework.test import APITestCase
from unittest import mock
from django.core.files import File
from django.urls import reverse
from noteally_app.tests.fill_db import fill_db
from rest_framework.exceptions import ErrorDetail
from noteally_app.models import User


class TestAuthView(APITestCase):
    
    def setUp(self):
        self = fill_db(self) 

        self.url = reverse('register')


    def test_register_success(self): 
        
        # form data
        data = { 
            "name": "Teles",
            "description": "Hello Im Teles",
            "email": "telesss@ua.pt",
            "university": self.university1.id,
            "tutoring_services": True,
            "password": "secret",
            "id_aws":0
        }
        response = self.client.post(self.url, data, format='multipart')
        
        expected_response = {
            "Success": "Successfully Registered"
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 200)
        
        # Assert the response data
        self.assertEqual(response.data['Success'], expected_response['Success'])
        
    def test_login_success(self): 
        
        # form data
        data = { 
            "name": "Teles",
            "description": "Hello Im Teles",
            "email": "telesss@ua.pt",
            "university": self.university1.id,
            "tutoring_services": True,
            "password": "secret",
            "id_aws":0
        }
        response = self.client.post(self.url, data, format='multipart')
        
        expected_response = {
            "Success": "Successfully Registered"
        }
        
        
        # form data
        data = { 
            "email": "telesss@ua.pt",
            "password": "secret", 
        }
        response = self.client.post( reverse('login'), data, format='multipart')
        
        expected_response = {
            "Success": "Successfully Logged",
            "id": 3,
            "name": "Teles",
            "email": "telesss@ua.pt"
            
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 200)
        
        # Assert the response data
        self.assertEqual(response.data['Success'], expected_response['Success'])
        self.assertEqual(response.data['id'], expected_response['id'])
        self.assertEqual(response.data['name'], expected_response['name'])
        self.assertEqual(response.data['email'], expected_response['email'])
        
    

 
