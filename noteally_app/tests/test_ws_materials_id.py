from rest_framework.test import APITestCase
from django.urls import reverse
from noteally_app.tests.fill_db import fill_db
from django.db.models import Max
from noteally_app.models import Material


class TestMaterialsIDView(APITestCase):
    
    def setUp(self):
        self = fill_db(self)
        self.url = reverse('materials_id', kwargs={'material_id': self.material1.id})
        
    
    def test_get_material_id_success(self):
        response = self.client.get(self.url)
        
        # Assert the response status code
        self.assertEqual(response.status_code, 200)
        
        # Assert the response data
        self.assertEqual(response.data["id"], self.material1.id)

    
    
    def test_get_material_id_invalid_id(self):
        max_id = Material.objects.aggregate(max_id=Max('id'))['max_id']
        non_existent_id = max_id + 1 if max_id is not None else 1
        
        response = self.client.get(reverse('materials_id', kwargs={'material_id': non_existent_id}))
        
        expected_response = {
            'error': 'Material does not exist'
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 404)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)


    def test_get_material_link_with_file(self):

        url = reverse('materials_id_download', kwargs={'material_id': self.material1.id})
        response = self.client.get(url)
        
        expected_response = {
            'name': self.material1.file_name,
            'link': '/test_media/' + self.material1.file_name,
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)
    

    def test_get_material_link_with_no_file(self):

        url = reverse('materials_id_download', kwargs={'material_id': self.material2.id})
        response = self.client.get(url)
        
        expected_response = {
            'error': 'Material does not have a file'
        }
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)


    def test_get_material_link_invalid_id(self):
        max_id = Material.objects.aggregate(max_id=Max('id'))['max_id']
        non_existent_id = max_id + 1 if max_id is not None else 1
        
        url = reverse('materials_id_download', kwargs={'material_id': non_existent_id})
        response = self.client.get(url)
        
        expected_response = {
            'error': 'Material does not exist'
        }
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)
    