from rest_framework.test import APITestCase
from django.urls import reverse
from unittest import mock
from django.core.files import File
from noteally_app.tests.fill_db import fill_db
from noteally_app.models import Material
from django.db.models import Max
import shutil


class TestAuthView(APITestCase):
    
    def setUp(self):
        self = fill_db(self)
        self.url = reverse('update_profile')
        self.user_bearer_token = 'Bearer 0123456789'
        self.example_description = 'Updated description'


    def tearDown(self):
        shutil.rmtree('test_media', ignore_errors=True)
        

    def test_update_profile_success(self):
        headers = {'User-id': self.user1.id, 'Authorization': self.user_bearer_token}
        data = {
            'description': self.example_description,
            'study_areas': [self.study_area1.id]
        }

        response = self.client.post(self.url, data, format='json', headers=headers)
        self.assertEqual(response.status_code, 200)


    def test_update_profile_success_with_photo(self):

        # mock profile_picture file
        file_mock = mock.MagicMock(spec=File, name='FileMock')
        file_mock.name = 'profile_picture.jpg'

        # request data
        headers = {'User-id': self.user1.id, 'Authorization': self.user_bearer_token}
        data = {
            'description': self.example_description,
            'study_areas': [self.study_area1.id],
            'profile_picture': file_mock
        }

        response = self.client.post(self.url, data, format='multipart', headers=headers)
        self.assertEqual(response.status_code, 200)


    def test_update_profile_missing_data(self):
        headers = {'User-id': self.user1.id, 'Authorization': self.user_bearer_token}
        data = {
            'description': 'Updated description'
        }

        response = self.client.post(self.url, data, format='json', headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Invalid data')
        

    def test_update_profile_user_not_in_database(self):
        max_id = Material.objects.aggregate(max_id=Max('id'))['max_id']
        non_existent_id = max_id + 2 if max_id is not None else 1
    
        headers = {'User-id': non_existent_id, 'Authorization': self.user_bearer_token}
        data = {
            'id_token': '0123456789',
            'description': self.example_description,
            'study_areas': [self.study_area1.id]
        }

        response = self.client.post(self.url, data, format='json', headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'User not in database')
