from rest_framework.test import APITestCase
from django.urls import reverse
from noteally_app.tests.fill_db import fill_db
from noteally_app.models import Material
from django.db.models import Max


class TestDownloadsView(APITestCase):
    
    def setUp(self):
        self = fill_db(self)
        self.error_response = {'error': 'Error while getting posts'}


    def test_get_posts(self):
        url = reverse('posts')
        headers = {'User-id': self.user1.id}
        response = self.client.get(url, headers=headers)
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Material.objects.filter(user=self.user1).count())


    # get posts with no headers
    def test_get_posts_invalid(self):
        url = reverse('posts')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, self.error_response)


    def test_delete_post(self):
        headers = {'User-id': self.user1.id}
        url = reverse('posts_id', kwargs={'material_id': self.material1.id})
        response = self.client.delete(url, headers=headers)
        expected_response = {'success': 'Post deleted'}
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)


    def test_delete_non_existing_post(self):
        max_id = Material.objects.aggregate(max_id=Max('id'))['max_id']
        non_existent_id = max_id + 1 if max_id is not None else 1

        headers = {'User-id': self.user1.id}
        url = reverse('posts_id', kwargs={'material_id': non_existent_id})
        response = self.client.delete(url, headers=headers)
        expected_response = {'error': 'Post does not exist'}
    
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected_response)


    # delete post with no headers
    def test_delete_post_invalid(self):
        url = reverse('posts_id', kwargs={'material_id': self.material1.id})
        response = self.client.delete(url)
    
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, self.error_response)

    # get posts with valid user_id
    def test_get_posts_by_user(self):
        url = reverse('posts_user_id', kwargs={'user_id': self.user1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Material.objects.filter(user=self.user1).count())

    # get posts with invalid user_id
    def test_get_posts_by_user_invalid(self):
        url = reverse('posts_user_id', kwargs={'user_id': 999})  # Use an invalid user_id
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, self.error_response)
