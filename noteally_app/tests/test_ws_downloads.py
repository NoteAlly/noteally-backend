from rest_framework.test import APITestCase
from django.urls import reverse
from noteally_app.tests.fill_db import fill_db
from django.db.models import Max
from noteally_app.models import Material
from noteally_app.models import Download


class TestDownloadsView(APITestCase):
    
    def setUp(self):
        self = fill_db(self)


    def test_download_material(self):
        headers = {'User-id': self.user3.id}
        url = reverse('downloads_id', kwargs={'material_id': self.material1.id})

        response = self.client.get(url, headers=headers)
        
        expected_response = {
            'name': self.material1.file_name,
            'link': '/test_media/' + self.material1.file_name,
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], expected_response['name'])

        downloaded = Download.objects.filter(user=self.user3, resource=self.material1).exists()
        self.assertTrue(downloaded)
    

    def test_download_material_invalid_id(self):
        max_id = Material.objects.aggregate(max_id=Max('id'))['max_id']
        non_existent_id = max_id + 1 if max_id is not None else 1
        
        headers = {'User-id': self.user3.id}
        url = reverse('downloads_id', kwargs={'material_id': non_existent_id})
        response = self.client.get(url, headers=headers)
        
        expected_response = {
            'error': 'Error while downloading material'
        }
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected_response)

        downloaded = Download.objects.filter(user=self.user3, resource=non_existent_id).exists()
        self.assertFalse(downloaded)


    def test_get_downloads_success(self):
        headers = {'User-id': self.user3.id}
        url = reverse('downloads')
        response = self.client.get(url, headers=headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)


    def test_get_downloads_invalid(self):
        url = reverse('downloads')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)

