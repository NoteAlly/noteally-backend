from rest_framework.test import APITestCase
from unittest import mock
from django.core.files import File
from django.urls import reverse
from noteally_app.models import Material
from django.db.models import Max
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
            "university": self.university1.id,
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
            "university": self.university1.id,
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
            "university": self.university1.id,
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


    def test_get_materials_no_filter(self):
        response = self.client.get(self.url, format='multipart')

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the response data
        self.assertEquals(len(response.data['results']), 2)

    
    def test_get_materials_match(self):
        data = {
            "title": "Calculus",
            "author": "John",
            "study_area": self.study_area2.id,
            "university": self.university2.id,
            "min_likes": 0,
            "min_downloads": 0,
            "free": "true",
            "order_by": "-total_downloads"
        }

        response = self.client.get(self.url, data, format='multipart')

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # should exist 1 match
        self.assertEquals(len(response.data['results']), 1)

        # Assert the response data
        self.assertEquals(response.data['results'][0]['id'], self.material2.id)


    def test_get_materials_no_match(self):
        data = {
            "free": "false",
            "max_price": 5
        }

        response = self.client.get(self.url, data, format='multipart')

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # should exist 0 match
        self.assertEquals(len(response.data['results']), 0)
    

class TestMaterialsIDView(APITestCase):
    
    def setUp(self):
        self = fill_db(self)
        self.url = reverse('materials_id', kwargs={'material_id': self.material1.id})
        
    
    def test_get_material_id_success(self):
        response = self.client.get(self.url, format='multipart')
        
        expected_response = {
            'id': self.material1.id,
            'upload_date': self.material1.upload_date.strftime("%d/%m/%Y %H:%M:%S"),
            'name': 'Introduction to Programming',
            'description': 'Introduction to Programming',
            'price': 0,
            'file_name': 'introduction_to_programming.pdf',
            'file': '/https%3A/noteally.s3.eu-west-3.amazonaws.com/introduction_to_programming.pdf',
            'total_likes': 0,
            'total_dislikes': 0,
            'total_downloads': 0,
            # user : ('id', 'name', 'email', 'karma_score', 'description', 'tutoring_services', 'profile_picture_link', 'university', 'study_areas')
            'user': {
                'id': self.user1.id,
                'name': 'John',
                'email': 'john@ua.pt',
                'karma_score': 0,
                'description': "I'm a student at the University of Aveiro.",
                'tutoring_services': True,
                'profile_picture_link': 'https://noteally.s3.eu-west-3.amazonaws.com/john.jpg',
                'university': {
                    'id': self.university1.id,
                    'name': 'University of Aveiro',
                },
                'study_areas': [
                ],
            },
            'university': {
                'id': self.university1.id,
                'name': 'University of Aveiro',
            },
            'study_areas': [
                {
                    'id': self.study_area1.id,
                    'name': 'Computer Science',
                },
            ],
        }
        
        
        # # Assert the response status code
        self.assertEqual(response.status_code, 200)
        
        # # # Assert the response data
        self.assertEqual(response.data, expected_response)
    
    
    def test_get_material_id_invalid_id(self):
        max_id = Material.objects.aggregate(max_id=Max('id'))['max_id']
        non_existent_id = max_id + 1 if max_id is not None else 1
        
        response = self.client.get(reverse('materials_id', kwargs={'material_id': non_existent_id}), format='multipart')
        
        expected_response = {
            'error': 'Material does not exist'
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 404)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
        
