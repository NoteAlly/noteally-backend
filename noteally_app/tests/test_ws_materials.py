from rest_framework.test import APITestCase
from unittest import mock
from django.core.files import File
from django.urls import reverse
from noteally_app.tests.fill_db import fill_db
from rest_framework.exceptions import ErrorDetail
import shutil


class TestMaterialsView(APITestCase):
    
    def setUp(self):
        self = fill_db(self)
        self.header = {'User-id': self.user1.id}
        self.url = reverse('materials')


    def tearDown(self):
        shutil.rmtree('test_media', ignore_errors=True)


    def test_post_material_success(self):
        file_mock = mock.MagicMock(spec=File, name="FileMock")
        file_mock.name = 'test.pdf'
        
        # form data
        data = {
            "user": self.user1.id,
            "name": "Introduction to Programming1",
            "description": "Introduction to Programming1",
            "price": 0,
            "university": self.university1.id,
            "file": file_mock,
            "study_areas": [self.study_area1.id, self.study_area2.id],
        }

        response = self.client.post(self.url, data, headers=self.header, format='multipart')
        
        expected_response = {
            "Success": "Successfully Created",
            "created_id": response.data['created_id'],
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 201)
        
        # Assert the response data
        self.assertEqual(response.data['Success'], expected_response['Success'])
        
    
    def test_post_material_invalid_file(self):
        data = {
            "user": self.user1.id,
            "name": "Introduction to Programming2",
            "description": "Introduction to Programming2",
            "price": 0,
            "university": self.university1.id,
            "file": "string_instead_of_file",
            "study_areas": [self.study_area1.id, self.study_area2.id],
        }

        response = self.client.post(self.url, data, headers=self.header, format='multipart')
        
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
        data = {
            "user": self.user1.id,
            "name": "Introduction to Programming3",
            "description": "Introduction to Programming3",
            "price": 0,
            "university": self.university1.id,
            "study_areas": [self.study_area1.id, self.study_area2.id],
        }
        
        response = self.client.post(self.url, data, headers=self.header, format='multipart')
        
        expected_response = {
            "Success": "Successfully Created",
            "created_id": response.data['created_id'],
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 201)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)


    def test_get_materials_no_filter(self):
        response = self.client.get(self.url)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the response data
        self.assertEquals(len(response.data['results']), 2)

    
    def test_get_materials_match_1(self):
        data = {
            "name": "Calculus",
            "author": "John Doe",
            "study_area": self.study_area2.id,
            "university": self.university2.id,
            "min_likes": 0,
            "min_downloads": 0,
            "free": "true",
            "order_by": "-total_downloads"
        }

        response = self.client.get(self.url, data)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # should exist 1 match
        self.assertEquals(len(response.data['results']), 1)

        # Assert the response data
        self.assertEquals(response.data['results'][0]['id'], self.material2.id)


    def test_get_materials_match_2(self):
        data = {
            "name": "Calculus",
            "author": "John",
            "study_area": self.study_area2.id,
            "university": self.university2.id,
            "min_likes": 0,
            "min_downloads": 0,
            "free": "true",
            "order_by": "-total_downloads"
        }

        response = self.client.get(self.url, data)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # should exist 1 match
        self.assertEquals(len(response.data['results']), 1)

        # Assert the response data
        self.assertEquals(response.data['results'][0]['id'], self.material2.id)
