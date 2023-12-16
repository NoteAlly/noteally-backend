from rest_framework.test import APITestCase
from django.urls import reverse
from noteally_app.tests.fill_db import fill_db
from django.db.models import Max
from noteally_app.models import Material


class TestMaterialsIDView(APITestCase):
    
    def setUp(self):
        self = fill_db(self)
        
    
    def test_get_material_id_success(self):
        headers = {'User-id': self.user1.id}
        url = reverse('materials_id', kwargs={'material_id': self.material1.id})
        response = self.client.get(url, headers=headers)
        
        # Assert the response status code
        self.assertEqual(response.status_code, 200)
        
        # Assert the response data
        self.assertEqual(response.data["id"], self.material1.id)

    
    
    def test_get_material_id_invalid_id(self):
        max_id = Material.objects.aggregate(max_id=Max('id'))['max_id']
        non_existent_id = max_id + 1 if max_id is not None else 1
        
        headers = {'User-id': self.user1.id}
        url = reverse('materials_id', kwargs={'material_id': non_existent_id})
        response = self.client.get(url, headers=headers)
        
        expected_response = {
            'error': 'Material does not exist'
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 404)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
