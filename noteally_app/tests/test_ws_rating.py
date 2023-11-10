from rest_framework.test import APITestCase
from django.urls import reverse
from noteally_app.tests.fill_db import fill_db
from noteally_app.models import Like, Material, User
from django.db.models import Max


class TestMaterialsView(APITestCase):
    
    def setUp(self):
        self = fill_db(self)
        self.header = {'User-id': self.user1.id}



    def test_like(self):
        # get karma score, likes and dislikes
        karma_score = User.objects.get(id=self.user1.id).karma_score
        likes = Material.objects.get(id=self.material2.id).total_likes
        dislikes = Material.objects.get(id=self.material2.id).total_dislikes

        # api request
        url = reverse('like', kwargs={'material_id': self.material2.id})
        response = self.client.post(url, headers=self.header)
        expected_response = {"Success": "Successfully Liked"}
        
        # assertions
        user = User.objects.get(id=self.user1.id)
        material = Material.objects.get(id=self.material2.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

        self.assertTrue(Like.objects.filter(user=user, resource=material).exists())
        self.assertEqual(material.total_likes, likes + 1)
        self.assertEqual(material.total_dislikes, dislikes)
        self.assertEqual(user.karma_score, karma_score + 3)



    def test_like_already_liked(self):
        # get karma score, likes and dislikes
        karma_score = User.objects.get(id=self.user1.id).karma_score
        likes = Material.objects.get(id=self.material2.id).total_likes
        dislikes = Material.objects.get(id=self.material2.id).total_dislikes

        # api request
        url = reverse('like', kwargs={'material_id': self.material1.id})
        response = self.client.post(url, headers=self.header)
        expected_response = {"Success": "Already Liked"}
        
        # assertions
        user = User.objects.get(id=self.user1.id)
        material = Material.objects.get(id=self.material1.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

        self.assertTrue(Like.objects.filter(user=user, resource=material).exists())
        self.assertEqual(material.total_likes, likes)
        self.assertEqual(material.total_dislikes, dislikes)
        self.assertEqual(user.karma_score, karma_score)



    def test_like_when_disliked(self):
        # add dislike
        url = reverse('dislike', kwargs={'material_id': self.material2.id})
        response = self.client.post(url, headers=self.header)

        # get karma score, likes and dislikes
        karma_score = User.objects.get(id=self.user1.id).karma_score
        likes = Material.objects.get(id=self.material2.id).total_likes
        dislikes = Material.objects.get(id=self.material2.id).total_dislikes

        # api request
        url = reverse('like', kwargs={'material_id': self.material2.id})
        response = self.client.post(url, headers=self.header)
        expected_response = {"Success": "Successfully Liked"}
        
        # assertions
        user = User.objects.get(id=self.user1.id)
        material = Material.objects.get(id=self.material2.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

        self.assertTrue(Like.objects.filter(user=user, resource=material).exists())
        self.assertEqual(material.total_likes, likes+1)
        self.assertEqual(material.total_dislikes, dislikes - 1)
        self.assertEqual(user.karma_score, karma_score + 3)



    def test_like_invalid_material(self):
        max_id = Material.objects.aggregate(max_id=Max('id'))['max_id']
        non_existent_id = max_id + 1 if max_id is not None else 1

        # api request
        url = reverse('like', kwargs={'material_id': non_existent_id})
        response = self.client.post(url, headers=self.header)
        expected_response = {"error": "Material does not exist"}
        
        # assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)



    def test_unlike(self):
        # add like
        url = reverse('like', kwargs={'material_id': self.material2.id})
        response = self.client.post(url, headers=self.header)

        # get karma score, likes and dislikes
        karma_score = User.objects.get(id=self.user1.id).karma_score
        likes = Material.objects.get(id=self.material2.id).total_likes
        dislikes = Material.objects.get(id=self.material2.id).total_dislikes

        # api request
        url = reverse('like', kwargs={'material_id': self.material2.id})
        response = self.client.delete(url, headers=self.header)
        expected_response = {"Success": "Successfully deleted"}
        
        # assertions
        user = User.objects.get(id=self.user1.id)
        material = Material.objects.get(id=self.material2.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

        self.assertFalse(Like.objects.filter(user=user, resource=material).exists())
        self.assertEqual(material.total_likes, likes - 1)
        self.assertEqual(material.total_dislikes, dislikes)
        self.assertEqual(user.karma_score, karma_score-3)



    def test_unlike_invalid_material(self):
        max_id = Material.objects.aggregate(max_id=Max('id'))['max_id']
        non_existent_id = max_id + 1 if max_id is not None else 1

        # api request
        url = reverse('like', kwargs={'material_id': non_existent_id})
        response = self.client.delete(url, headers=self.header)
        expected_response = {"error": "Material does not exist"}
        
        # assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)



    def test_dislike(self):
        # get karma score, likes and dislikes
        karma_score = User.objects.get(id=self.user1.id).karma_score
        likes = Material.objects.get(id=self.material2.id).total_likes
        dislikes = Material.objects.get(id=self.material2.id).total_dislikes

        # api request
        url = reverse('dislike', kwargs={'material_id': self.material2.id})
        response = self.client.post(url, headers=self.header)
        expected_response = {"Success": "Successfully Disliked"}
        
        # assertions
        user = User.objects.get(id=self.user1.id)
        material = Material.objects.get(id=self.material2.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

        self.assertTrue(Like.objects.filter(user=user, resource=material).exists())
        self.assertEqual(material.total_likes, likes)
        self.assertEqual(material.total_dislikes, dislikes + 1)
        self.assertEqual(user.karma_score, karma_score)



    def test_dislike_already_disliked(self):
        # add dislike
        url = reverse('dislike', kwargs={'material_id': self.material2.id})
        response = self.client.post(url, headers=self.header)

        # get karma score, likes and dislikes
        karma_score = User.objects.get(id=self.user1.id).karma_score
        likes = Material.objects.get(id=self.material2.id).total_likes
        dislikes = Material.objects.get(id=self.material2.id).total_dislikes

        # api request
        url = reverse('dislike', kwargs={'material_id': self.material2.id})
        response = self.client.post(url, headers=self.header)
        expected_response = {"Success": "Already Disliked"}
        
        # assertions
        user = User.objects.get(id=self.user1.id)
        material = Material.objects.get(id=self.material2.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

        self.assertTrue(Like.objects.filter(user=user, resource=material).exists())
        self.assertEqual(material.total_likes, likes)
        self.assertEqual(material.total_dislikes, dislikes)
        self.assertEqual(user.karma_score, karma_score)



    def test_dislike_when_liked(self):
        # add like
        url = reverse('like', kwargs={'material_id': self.material2.id})
        response = self.client.post(url, headers=self.header)

        # get karma score, likes and dislikes
        karma_score = User.objects.get(id=self.user1.id).karma_score
        likes = Material.objects.get(id=self.material2.id).total_likes
        dislikes = Material.objects.get(id=self.material2.id).total_dislikes

        # api request
        url = reverse('dislike', kwargs={'material_id': self.material2.id})
        response = self.client.post(url, headers=self.header)
        expected_response = {"Success": "Successfully Disliked"}
        
        # assertions
        user = User.objects.get(id=self.user1.id)
        material = Material.objects.get(id=self.material2.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

        self.assertTrue(Like.objects.filter(user=user, resource=material).exists())
        self.assertEqual(material.total_likes, likes - 1)
        self.assertEqual(material.total_dislikes, dislikes+1)
        self.assertEqual(user.karma_score, karma_score-3)



    def test_dislike_invalid_material(self):
        max_id = Material.objects.aggregate(max_id=Max('id'))['max_id']
        non_existent_id = max_id + 1 if max_id is not None else 1

        # api request
        url = reverse('dislike', kwargs={'material_id': non_existent_id})
        response = self.client.post(url, headers=self.header)
        expected_response = {"error": "Material does not exist"}
        
        # assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)



    def test_undislike(self):
        # add dislike
        url = reverse('dislike', kwargs={'material_id': self.material2.id})
        response = self.client.post(url, headers=self.header)

        # get karma score, likes and dislikes
        karma_score = User.objects.get(id=self.user1.id).karma_score
        likes = Material.objects.get(id=self.material2.id).total_likes
        dislikes = Material.objects.get(id=self.material2.id).total_dislikes

        # api request
        url = reverse('dislike', kwargs={'material_id': self.material2.id})
        response = self.client.delete(url, headers=self.header)
        expected_response = {"Success": "Successfully deleted"}
        
        # assertions
        user = User.objects.get(id=self.user1.id)
        material = Material.objects.get(id=self.material2.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

        self.assertFalse(Like.objects.filter(user=user, resource=material).exists())
        self.assertEqual(material.total_likes, likes)
        self.assertEqual(material.total_dislikes, dislikes - 1)
        self.assertEqual(user.karma_score, karma_score)



    def test_undislike_invalid_material(self):
        max_id = Material.objects.aggregate(max_id=Max('id'))['max_id']
        non_existent_id = max_id + 1 if max_id is not None else 1

        # api request
        url = reverse('dislike', kwargs={'material_id': non_existent_id})
        response = self.client.delete(url, headers=self.header)
        expected_response = {"error": "Material does not exist"}
        
        # assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response)
