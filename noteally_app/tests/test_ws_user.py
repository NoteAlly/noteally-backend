from rest_framework.test import APITestCase
from django.urls import reverse
from noteally_app.tests.fill_db import fill_db
from django.db.models import Max
from noteally_app.models import User

# import ErrorDetail in the line below
from rest_framework.exceptions import ErrorDetail


class TestUserView(APITestCase):
    
    def setUp(self):
        self = fill_db(self)
        
    def test_unlock_premium(self):
        assert self.user2.premium == False
        
        url = reverse('unlock_premium')
        headers = {'User-id': self.user2.id}
        
        response = self.client.post(url, headers=headers)
        
        expected_response = {
            'user_id': self.user2.id,
            'message': 'Premium unlocked'
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 200)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
    
    
    def test_unlock_premium_already_premium(self):
        assert self.user1.premium == True
        
        url = reverse('unlock_premium')
        headers = {'User-id': self.user1.id}
        
        response = self.client.post(url, headers=headers)
        
        expected_response = {
            'error': 'User is already premium'
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 400)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
        
    
    def test_unlock_premium_invalid_id(self):
        max_id = User.objects.aggregate(max_id=Max('id'))['max_id']
        non_existent_id = max_id + 1 if max_id is not None else 1
        
        url = reverse('unlock_premium')
        headers = {'User-id': non_existent_id}
        
        response = self.client.post(url, headers=headers)
        
        expected_response = {
            'error': 'User not found'
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 400)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
        
    
    def test_unlock_premium_no_id(self):
        url = reverse('unlock_premium')
        
        response = self.client.post(url)
        
        expected_response = {
            'error': 'User-id header not found'
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 400)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
    
    
    def test_unlock_premium_get_method(self):
        url = reverse('unlock_premium')
        headers = {'User-id': self.user1.id}
        
        response = self.client.get(url, headers=headers)
        
        expected_response = {
            'detail': ErrorDetail(string='Method "GET" not allowed.', code='method_not_allowed')
        }
           
        # Assert the response status code
        self.assertEqual(response.status_code, 405)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
        
        
        
        