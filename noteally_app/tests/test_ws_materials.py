from rest_framework.test import APIRequestFactory, APITestCase

from unittest import skip, skipIf, skipUnless

# Mocking
from unittest import mock
from django.core.files import File

from django.urls import reverse

from noteally_app.tests.fill_db import fill_db

from rest_framework.exceptions import ErrorDetail

class TestMaterialsView(APITestCase):
    
    def setUp(self):
        self = fill_db(self)
        self.url = reverse('materials')
        
    def test_post_material_success(self):
        file_mock = mock.MagicMock(spec=File, name="FileMock")
        file_mock.name = 'test.pdf'
        
        # form data
        data = {
            "user": self.user1.id,
            "name": "Introduction to Programming1",
            "description": "Introduction to Programming1",
            "price": 0,
            "university": "University of Aveiro1",
            "file": file_mock,
            "study_areas": [self.study_area1.id, self.study_area2.id],
        }
        response = self.client.post(self.url, data, format='multipart')
        
        expected_response = {
            "Success": "Successfully Created",
            "created_id": response.data['created_id'],
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 201)
        
        # Assert the response data
        self.assertEqual(response.data['Success'], expected_response['Success'])
        
    
    def test_post_material_invalid_file(self):
        #form data
        data = {
            "user": self.user1.id,
            "name": "Introduction to Programming2",
            "description": "Introduction to Programming2",
            "price": 0,
            "university": "University of Aveiro2",
            "file": "string_instead_of_file",
            "study_areas": [self.study_area1.id, self.study_area2.id],
        }
        
        response = self.client.post(self.url, data, format='multipart')
        
        expected_response = {
            'error': {
                'file': [ErrorDetail(string='The submitted data was not a file. Check the encoding type on the form.', code='invalid')]
                }
            }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 400)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
        
    
    def test_post_material_no_file(self):
        #form data
        data = {
            "user": self.user1.id,
            "name": "Introduction to Programming3",
            "description": "Introduction to Programming3",
            "price": 0,
            "university": "University of Aveiro3",
            "study_areas": [self.study_area1.id, self.study_area2.id],
        }
        
        response = self.client.post(self.url, data, format='multipart')
        
        expected_response = {
            "Success": "Successfully Created",
            "created_id": response.data['created_id'],
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 201)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
        
        
        
        