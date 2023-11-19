from rest_framework.test import APITestCase
from unittest import mock
from django.core.files import File
from django.urls import reverse
from noteally_app.tests.fill_db import fill_db
from rest_framework.exceptions import ErrorDetail
import shutil
from noteally_app.models import StudyArea, User

 
def setUp(self):
    # Set up any necessary data for your tests
    self.url = reverse('get_tutors')  # Update with your actual URL for the get_tutors endpoint
    self.user1 = User.objects.create(username='tutor1', first_name='John', last_name='Doe', karma_score=5)
    self.user2 = User.objects.create(username='tutor2', first_name='Jane', last_name='Smith', karma_score=10)
    self.user3 = User.objects.create(username='tutor3', first_name='Bob', last_name='Johnson', karma_score=8)

def test_get_tutors_no_filter(self):
    response = self.client.get(self.url)

    # Assert the response status code
    self.assertEqual(response.status_code, 200)

    # Assert the response data
    self.assertEquals(len(response.data['results']), 3)

def test_get_tutors_filter_karma_score(self):
    data = {"karma_score": 9}

    response = self.client.get(self.url, data)

    # Assert the response status code
    self.assertEqual(response.status_code, 200)

    # should exist 2 matches
    self.assertEquals(len(response.data['results']), 2)

    # Assert the response data
    self.assertIn(self.user2.id, [user['id'] for user in response.data['results']])
    self.assertIn(self.user3.id, [user['id'] for user in response.data['results']])

def test_get_tutors_filter_study_areas(self):
    # Assuming study areas are associated with users in your actual implementation
    study_area = StudyArea.objects.create(name='Mathematics')
    self.user2.study_areas.add(study_area)

    data = {"study_areas": [study_area.id]}

    response = self.client.get(self.url, data)

    # Assert the response status code
    self.assertEqual(response.status_code, 200)

    # should exist 1 match
    self.assertEquals(len(response.data['results']), 1)

    # Assert the response data
    self.assertEquals(response.data['results'][0]['id'], self.user2.id)

def test_get_tutors_filter_name(self):
    data = {"name": "John Doe"}

    response = self.client.get(self.url, data)

    # Assert the response status code
    self.assertEqual(response.status_code, 200)

    # should exist 1 match
    self.assertEquals(len(response.data['results']), 1)

    # Assert the response data
    self.assertEquals(response.data['results'][0]['id'], self.user1.id)

def test_get_tutors_order_by_karma_score_desc(self):
    data = {"order_by": "-karma_score"}

    response = self.client.get(self.url, data)

    # Assert the response status code
    self.assertEqual(response.status_code, 200)

    # Assert the order of results based on karma score
    karma_scores = [user['karma_score'] for user in response.data['results']]
    self.assertEqual(karma_scores, [10, 8, 5])
